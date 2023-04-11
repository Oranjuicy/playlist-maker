import requests
from bs4 import BeautifulSoup
import spotipy
from urllib.error import HTTPError


with open("txt.cache") as token:
    TOKEN = token.read().split("]")[0]

ID = "b29a46f8a7ad436faf7efe14ed2c48ff"
SECRET = "14975b9886084e30be291189b25a8327"
REDIRECT_URI = "http://example.com"
# TOKEN = "BQDVgSYyOY-MhdQgkQHzFZsooOLldldLgsSRFMZZPDOtPhCdmtAOCM2jDv97P2QP6eHm0N2TkBrwiSvuhJrtQMEUjZ6ngN1k7Ogbsfw3jYjyuDY_mCSuKtUoOlIrzBxjgBGK8VNB6-08tJSvQp6ZNdXoKdtvdrjn12fnz9wvlzDaDXxYv_I9KadkBk-PKMqOEND0HZtr_hUXJROoyeTEuTff39bK3Yumh2eH6w"

date_to_search = input("Which date tickles your fancy (YYYY-MM-DD)?: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_to_search}/")

date_html = response.text

soup = BeautifulSoup(date_html, "html.parser")

song_tags = soup.select("li h3", class_="c-title")

song_names = [song.getText().strip() for song in song_tags]

# SPOTIFY

scope = "playlist-modify-public"

sp = spotipy.oauth2.SpotifyOAuth(client_id=ID, client_secret=SECRET, redirect_uri=REDIRECT_URI, scope=scope)

spotty = spotipy.client.Spotify(TOKEN)

user_id = spotty.current_user()["id"]

spotify_song_list = [spotty.search(song) for song in song_names]
song_URI = []

if len(song_URI) > 99:
    while len(song_URI) >= 100:
        song_URI.pop()

for song in spotify_song_list:
    try:
        song_URI.append(song["tracks"]["items"][0]["uri"])
        print((song["tracks"]["items"][0]["uri"]))
    except IndexError:
        print(f"{song} not found. Skipped!")


playlist_ID = spotty.user_playlist_create(user=user_id, name=f"{date_to_search} Billboard 100")

for song in song_URI:
    try:
        spotty.playlist_add_items(playlist_id=playlist_ID["id"], items=song)
    except HTTPError as err:
        if err.code == 401:
            print("Song not found. Skipped.")
        else:
            raise



