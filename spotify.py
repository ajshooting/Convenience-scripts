import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API のクライアント ID とクライアントシークレットを設定
client_id = ""
client_secret = ""

# Spotipy クライアントを初期化
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)


def search_track(track_name):
    # 曲名で検索
    results = sp.search(q=track_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_id = track["id"]

        # 曲の詳細を取得
        track_details = {
            "名前": track["name"],
            "アーティスト": ", ".join([artist["name"] for artist in track["artists"]]),
            "アルバム": track["album"]["name"],
            "リリース日": track["album"]["release_date"],
            "プレビューURL": track["preview_url"],
        }

        # 曲のオーディオ特徴量を取得
        audio_features = sp.audio_features(track_id)[0]
        track_details.update(
            {
                "アコースティック度": audio_features["acousticness"],
                "ダンス度": audio_features["danceability"],
                "エネルギー度": audio_features["energy"],
                "インストゥルメンタル度": audio_features["instrumentalness"],
                "ライブ度": audio_features["liveness"],
                "音量": audio_features["loudness"],
                "話し言葉度": audio_features["speechiness"],
                "感情度": audio_features["valence"],
                "テンポ": audio_features["tempo"],
                "キー": audio_features["key"],
                "モード": audio_features["mode"],
                "拍子記号": audio_features["time_signature"],
            }
        )

        return track_details
    else:
        return None


# 曲名を入力して検索
track_name = input("曲名を入力してください: ")
track_details = search_track(track_name)

if track_details:
    print("曲の詳細:")
    for key, value in track_details.items():
        print(f"{key}: {value}")
else:
    print("曲が見つかりませんでした。")
