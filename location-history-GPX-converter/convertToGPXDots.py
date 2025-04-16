import json
from datetime import datetime
import gpxpy.gpx

# JSONファイルを読み込む
with open('location-history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# GPXオブジェクトを作成
gpx = gpxpy.gpx.GPX()

# JSONデータを処理
for event in data:
    if 'visit' in event:  # 「visit」イベントのみを対象とする
        visit = event['visit']
        
        # 滞在場所の座標を解析（"geo:緯度,経度"形式）
        place_location = visit['topCandidate']['placeLocation'].split(':')[1].split(',')
        lat = float(place_location[0])  # 緯度
        lon = float(place_location[1])  # 経度
        
        # 滞在開始時間をISO 8601形式からパース
        start_time = datetime.fromisoformat(event['startTime'].replace('+09:00', '+0900'))
        
        # ウェイポイントを作成
        waypoint = gpxpy.gpx.GPXWaypoint(
            latitude=lat,
            longitude=lon,
            time=start_time,
            name=visit['topCandidate']['placeID'],  # 場所のIDを名前として使用
            description=f"Probability: {visit['probability']}"  # 確率を説明に追加
        )
        gpx.waypoints.append(waypoint)

# GPXをXML形式に変換
gpx_xml = gpx.to_xml()

# ファイルに保存
with open('visit_points.gpx', 'w', encoding='utf-8') as f:
    f.write(gpx_xml)

print("GPXファイルが生成されました: visit_points.gpx")