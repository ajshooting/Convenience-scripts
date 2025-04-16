# -*- coding: utf-8 -*-
import json
import argparse
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateutil_parser  # More robust ISO 8601 parsing
import gpxpy
import gpxpy.gpx
import sys
import logging

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_geouri(geo_uri):
    """'geo:lat,lon' 形式の文字列をパースし、(緯度, 経度) のタプルを返す。"""
    try:
        if geo_uri and geo_uri.startswith("geo:"):
            # "geo:" を除去し、"," で分割して float に変換
            coords = geo_uri.split(":")[1]
            lat, lon = map(float, coords.split(","))
            # 緯度経度の基本的なバリデーション
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            else:
                logging.warning(
                    f"Invalid coordinate values: lat={lat}, lon={lon} from URI: {geo_uri}"
                )
                return None, None
        else:
            logging.warning(f"Invalid geo URI format: {geo_uri}")
            return None, None
    except Exception as e:
        logging.error(f"Error parsing geo URI '{geo_uri}': {e}")
        return None, None


def parse_isotime(time_str):
    """ISO 8601形式のタイムスタンプ文字列をパースし、タイムゾーン情報付きのdatetimeオブジェクトを返す。"""
    if not time_str:
        return None
    try:
        # dateutil.parser.isoparse はタイムゾーン情報 (+HH:MM や Z) を正しく解釈する
        dt = dateutil_parser.isoparse(time_str)
        return dt
    except ValueError as e:
        logging.error(f"Error parsing timestamp '{time_str}': {e}")
        return None
    except Exception as e:  # Handle other potential exceptions during parsing
        logging.error(
            f"An unexpected error occurred parsing timestamp '{time_str}': {e}"
        )
        return None


def load_json_data(json_filepath):
    """JSONファイルを読み込み、リスト形式で返す。"""
    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                if isinstance(data[key], list):
                    logging.info(
                        f"Detected nested list under key '{key}'. Processing list content."
                    )
                    return data[key]
            logging.error(
                "JSON structure is not a list or a dict with a single list element."
            )
            sys.exit(1)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON file '{json_filepath}': {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error reading JSON file '{json_filepath}': {e}")
        sys.exit(1)


def sort_data_by_start_time(data):
    """startTimeでデータをソート。"""

    def get_start_time_safe(item):
        dt = parse_isotime(item.get("startTime"))
        return dt if dt else datetime.min.replace(tzinfo=timezone.utc)

    try:
        data.sort(key=get_start_time_safe)
        logging.info("Data sorted by startTime.")
    except Exception as e:
        logging.warning(
            f"Could not sort data by startTime, processing in original order: {e}"
        )


def add_timeline_path_to_gpx(item, gpx, start_time, start_time_str):
    """timelinePathをGPXトラックとして追加。"""
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    gpx.tracks.append(gpx_track)
    gpx_track.name = f"Track starting at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    points_in_segment = 0
    for point_data in item["timelinePath"]:
        geo_uri = point_data.get("point")
        offset_minutes_str = point_data.get("durationMinutesOffsetFromStartTime")
        if not geo_uri or offset_minutes_str is None:
            logging.warning(
                f"Skipping point in timelinePath due to missing 'point' or 'durationMinutesOffsetFromStartTime': {point_data}"
            )
            continue
        lat, lon = parse_geouri(geo_uri)
        if lat is None or lon is None:
            logging.warning(f"Skipping point due to invalid geo URI: {geo_uri}")
            continue
        try:
            offset_minutes = float(offset_minutes_str)
            point_time = start_time + timedelta(minutes=offset_minutes)
        except Exception as e:
            logging.warning(
                f"Skipping point due to invalid offset '{offset_minutes_str}': {e}"
            )
            continue
        gpx_point = gpxpy.gpx.GPXTrackPoint(
            latitude=lat, longitude=lon, time=point_time
        )
        gpx_segment.points.append(gpx_point)
        points_in_segment += 1
    if points_in_segment == 0:
        gpx.tracks.remove(gpx_track)
        logging.warning(
            f"TimelinePath segment from {start_time_str} resulted in no valid points and was removed."
        )
        return False
    logging.info(
        f"Added timelinePath segment from {start_time_str} with {points_in_segment} points."
    )
    return True


def add_visit_to_gpx(item, gpx, start_time, start_time_str, end_time_str):
    """visitをGPXウェイポイントとして追加。"""
    visit_info = item.get("visit", {})
    top_candidate = visit_info.get("topCandidate", {})
    geo_uri = top_candidate.get("placeLocation")
    place_id = top_candidate.get("placeID", "N/A")
    semantic_type = top_candidate.get("semanticType", "Visit")
    probability = top_candidate.get("probability", "N/A")
    if geo_uri:
        lat, lon = parse_geouri(geo_uri)
        if lat is not None and lon is not None:
            gpx_waypoint = gpxpy.gpx.GPXWaypoint(
                latitude=lat,
                longitude=lon,
                time=start_time,
                name=f"{semantic_type} ({probability})",
                description=f"Visit from {start_time_str} to {end_time_str or '?'}. PlaceID: {place_id}",
                type=semantic_type,
            )
            gpx.waypoints.append(gpx_waypoint)
            logging.info(
                f"Added visit waypoint: {semantic_type} at {lat},{lon} for time {start_time_str}."
            )
            return True
        else:
            logging.warning(
                f"Could not add visit waypoint for {start_time_str}, invalid geo URI: {geo_uri}"
            )
    else:
        logging.warning(
            f"Visit item found from {start_time_str} but missing 'placeLocation'."
        )
    return False


def add_activity_waypoints_to_gpx(
    item, gpx, start_time, end_time, start_time_str, end_time_str
):
    """activityの開始・終了地点をウェイポイントとして追加。"""
    activity_info = item.get("activity", {})
    start_geo = activity_info.get("start")
    end_geo = activity_info.get("end")
    activity_type = activity_info.get("topCandidate", {}).get(
        "type", "Unknown Activity"
    )
    distance = activity_info.get("distanceMeters", "N/A")
    count = 0
    if start_geo:
        lat, lon = parse_geouri(start_geo)
        if lat is not None and lon is not None:
            wpt_start = gpxpy.gpx.GPXWaypoint(
                latitude=lat,
                longitude=lon,
                time=start_time,
                name=f"Start: {activity_type}",
                description=f"Activity started at {start_time_str}. Est. distance: {distance}m",
                type=f"Activity Start ({activity_type})",
            )
            gpx.waypoints.append(wpt_start)
            count += 1
    if end_geo and end_time:
        lat, lon = parse_geouri(end_geo)
        if lat is not None and lon is not None:
            wpt_end = gpxpy.gpx.GPXWaypoint(
                latitude=lat,
                longitude=lon,
                time=end_time,
                name=f"End: {activity_type}",
                description=f"Activity ended at {end_time_str}. Est. distance: {distance}m",
                type=f"Activity End ({activity_type})",
            )
            gpx.waypoints.append(wpt_end)
            count += 1
    elif end_geo and not end_time:
        logging.warning(
            f"Activity item has 'end' location ({end_geo}) but no valid 'endTime'. End waypoint not created for start time {start_time_str}."
        )
    return count


def convert_json_to_gpx(json_filepath, gpx_filepath):
    """入力JSONファイルをGPX形式に変換する。"""
    data = load_json_data(json_filepath)
    sort_data_by_start_time(data)
    gpx = gpxpy.gpx.GPX()
    gpx.creator = "JSON to GPX Conversion Script"
    processed_items = 0
    timeline_paths_processed = 0
    visits_processed = 0
    activity_waypoints_processed = 0

    for item in data:
        start_time_str = item.get("startTime")
        end_time_str = item.get("endTime")
        start_time = parse_isotime(start_time_str)
        if not start_time:
            logging.warning(
                f"Skipping item due to missing or invalid 'startTime': {item}"
            )
            continue
        end_time = parse_isotime(end_time_str)
        processed_items += 1

        if (
            "timelinePath" in item
            and isinstance(item["timelinePath"], list)
            and item["timelinePath"]
        ):
            if add_timeline_path_to_gpx(item, gpx, start_time, start_time_str):
                timeline_paths_processed += 1
        elif "visit" in item:
            if add_visit_to_gpx(item, gpx, start_time, start_time_str, end_time_str):
                visits_processed += 1
        elif "activity" in item:
            activity_waypoints_processed += add_activity_waypoints_to_gpx(
                item, gpx, start_time, end_time, start_time_str, end_time_str
            )
        else:
            logging.warning(
                f"Skipping unrecognized item structure starting at {start_time_str}: Keys={list(item.keys())}"
            )

    if not gpx.tracks and not gpx.waypoints:
        logging.warning(
            "No tracks or waypoints were generated from the JSON data. The output GPX file might be empty or contain only metadata."
        )
    else:
        logging.info(f"Summary: Processed {processed_items} items.")
        logging.info(
            f"Generated {len(gpx.tracks)} track(s) from {timeline_paths_processed} 'timelinePath' items."
        )
        logging.info(
            f"Generated {len(gpx.waypoints)} waypoint(s) ({visits_processed} from 'visit', {activity_waypoints_processed} from 'activity')."
        )

    try:
        gpx_xml = gpx.to_xml(version="1.1")
        with open(gpx_filepath, "w", encoding="utf-8") as f:
            f.write(gpx_xml)
        logging.info(f"Successfully wrote GPX data to '{gpx_filepath}'")
    except Exception as e:
        logging.error(f"Error writing GPX file '{gpx_filepath}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert JSON timeline data (potentially from Google Timeline) to GPX format."
    )
    parser.add_argument("json_file", help="Path to the input JSON file.")
    parser.add_argument("gpx_file", help="Path for the output GPX file.")
    args = parser.parse_args()
    convert_json_to_gpx(args.json_file, args.gpx_file)
