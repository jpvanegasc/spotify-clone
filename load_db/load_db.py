# TO-DO:
# * stablish ForeignKey relationships not by brute force
import json

import requests

PATH_TO_FILES = "./files"
LOCAL_URL = "http://localhost:8000/v1"

# Users

with open(f"{PATH_TO_FILES}/user.json") as f:
    user_original = json.loads(f.read())

user = {
    "country": user_original['country'],
    "display_name": user_original['display_name'],
    "email": user_original['email'],
    "href": user_original['href'],
    "id": user_original['id'],
    "product": user_original['product'],
    "type": user_original['type'],
    "uri": user_original['uri'],
}

r = requests.post(f"{LOCAL_URL}/users", json=user)

if r.ok:
    print("user loaded")
else:
    print(f"user failed. Endpoint response: {r.status_code} {r.text}")

# Playlists

with open(f"{PATH_TO_FILES}/playlists.json") as f:
    playlists = json.loads(f.read())

for playlist_original in playlists:
    playlist = {
        "collaborative": playlist_original['collaborative'],
        "description": playlist_original['description'],
        "href": playlist_original['href'],
        "id": playlist_original['id'],
        "name": playlist_original['name'],
        "owner_id":0,
        "public": playlist_original['public'],
        "snapshot_id": playlist_original['snapshot_id'],
        "type": playlist_original['type'],
        "uri": playlist_original['uri'],
    }

    r = requests.post(f"{LOCAL_URL}/playlists", json=playlist)

    if r.ok:
        print(f"{playlist['name']} loaded")
    else:
        print(f"{playlist['name']} failed. Endpoint response: {r.status_code} {r.text}")

# Artists

with open(f"{PATH_TO_FILES}/artists.json") as f:
    artists = json.loads(f.read())

for artist_original in artists:
    artist = {
        "href": artist_original['href'],
        "id": artist_original['id'],
        "name": artist_original['name'],
        "popularity": artist_original['popularity'],
        "type": artist_original['type'],
        "uri": artist_original['uri'],
    }
    r = requests.post(f"{LOCAL_URL}/artists", json=artist)

    if r.ok:
        print(f"{artist['name']} loaded")
    else:
        print(f"{artist['name']} failed. Endpoint response: {r.status_code} {r.text}")

# Albums

# with open(f"{PATH_TO_FILES}/albums.json") as f:
#     albums = json.loads(f.read())

# album_info = dict()

# for i, album_original in enumerate(albums):
#     if album_original['artists'][0]['name'] == "Rupatrupa":
#         artist = 0
#     else:
#         artist = 1

#     album = {
#         "album_type": album_original['album_type'],
#         "href": album_original['href'],
#         "id": album_original['id'],
#         "label": album_original['label'],
#         "name": album_original['name'],
#         "popularity": album_original['popularity'],
#         "total_tracks": album_original['total_tracks'],
#         "type": album_original['type'],
#         "uri": album_original['uri'],
#     }


#     album['artists_id'] = [artist]

#     album_info[album['name']] = {'album_id':i, 'artist_id':artist}

#     r = requests.post(f"{LOCAL_URL}/albums", json=album)

#     if r.ok:
#         print(f"{album['name']} loaded")
#     else:
#         print(f"{album['name']} failed. Endpoint response: {r.status_code} {r.text}")

# Tracks

# with open(f"{PATH_TO_FILES}/tracks.json") as f:
#     tracks = json.loads(f.read())

# for track_original in tracks:
#     album_name = track_original['album']['name']

#     track = {
#         "disc_number": track_original['disc_number'],
#         "duration_ms": track_original['duration_ms'],
#         "explicit": track_original['explicit'],
#         "href": track_original['href'],
#         "id": track_original['id'],
#         "is_local": track_original['is_local'],
#         "is_playable": track_original['is_playable'],
#         "name": track_original['name'],
#         "popularity": track_original['popularity'],
#         "preview_url": track_original['preview_url'],
#         "track_number": track_original['track_number'],
#         "type": track_original['type'],
#         "uri": track_original['uri'],
#     }

#     track['album_id'] = [album_info[album_name]['album_id']]
#     track['artist_id'] = [album_info[album_name]['artist_id']]

#     r = requests.post(f"{LOCAL_URL}/tracks", json=track)

#     if r.ok:
#         print(f"{track['name']} loaded")
#     else:
#         print(f"{track['name']} failed. Endpoint response: {r.status_code} {r.text}")
