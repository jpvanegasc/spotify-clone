# TO-DO:
# * stablish ForeignKey relationships not by brute force
import json

import requests

PATH_TO_FILES = "./files"
LOCAL_URL = "http://localhost:8000/v1"

def json_fields_to_str(json_object):
    """
    Convert json-like fields to str, in order to pass the objects to the api endpoints
    """
    for key in json_object.keys():
        if isinstance(json_object[key], (list, dict)):
            json_object[key] = str(json_object[key])

    return json_object

# Users

with open(f"{PATH_TO_FILES}/user.json") as f:
    user = json.loads(f.read())

r = requests.post(f"{LOCAL_URL}/users", data=json_fields_to_str(user))

if r.ok:
    print("user loaded")
else:
    print(f"user failed. Endpoint response: {r.json()}")

# Playlists

with open(f"{PATH_TO_FILES}/playlists.json") as f:
    playlists = json.loads(f.read())

for playlist in playlists:
    playlist.pop('owner', None)
    playlist.pop('tracks', None)

    r = requests.post(f"{LOCAL_URL}/playlists?user_id=0", data=json_fields_to_str(playlist))

    if r.ok:
        print(f"{playlist['name']} loaded")
    else:
        print(f"{playlist['name']} failed. Endpoint response: {r.json()}")

# Artists

with open(f"{PATH_TO_FILES}/artists.json") as f:
    artists = json.loads(f.read())

for artist in artists:
    r = requests.post(f"{LOCAL_URL}/artists", data=json_fields_to_str(artist))

    if r.ok:
        print(f"{artist['name']} loaded")
    else:
        print(f"{artist['name']} failed. Endpoint response: {r.json()}")

# Albums

with open(f"{PATH_TO_FILES}/albums.json") as f:
    albums = json.loads(f.read())

album_info = dict()

for i, album in enumerate(albums):
    if album['artists'][0]['name'] == "Rupatrupa":
        artist = 0
    else:
        artist = 1

    album.pop('artists', None)
    album.pop('tracks', None)
    album['artists_id'] = [artist]

    album_info[album['name']] = {'album_id':i, 'artist_id':artist}

    r = requests.post(f"{LOCAL_URL}/albums", data=json_fields_to_str(album))

    if r.ok:
        print(f"{album['name']} loaded")
    else:
        print(f"{album['name']} failed. Endpoint response: {r.json()}")

# Tracks

with open(f"{PATH_TO_FILES}/tracks.json") as f:
    tracks = json.loads(f.read())

for track in tracks:
    album_name = track['album']['name']

    track.pop('artists', None)
    track.pop('albums', None)
    track['album_id'] = [album_info[album_name]['album_id']]
    track['artist_id'] = [album_info[album_name]['artist_id']]

    r = requests.post(f"{LOCAL_URL}/tracks", data=json_fields_to_str(track))

    if r.ok:
        print(f"{track['name']} loaded")
    else:
        print(f"{track['name']} failed. Endpoint response: {r.json()}")
