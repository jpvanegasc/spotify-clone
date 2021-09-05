import json

import requests
from starlette.config import Config

SAVE_PATH = './files' # without the final '/'

config = Config('./.env')
TOKEN = config('SPOTIFY_ACCESS_TOKEN', cast=str)

headers = {
    'Content-Type':'application/json',
    'Authorization':f'Bearer {TOKEN}'
}

artists = {
    "Rupatrupa":{
        "id":"4NMzrymQlZzpXs0LT3Arei",
    },
    "Claire Laffut":{
        "id":"69zVBf7wk5vKWsTF7zE5CC"
    }
}

# Download Artists

artists_info = []
albums_ids = []

params = {
    'ids':','.join([artists[artist]['id'] for artist in artists])
}

r = requests.get("https://api.spotify.com/v1/artists", params=params, headers=headers)

if r.ok:
    artists_info = r.json()['artists']
else:
    raise Exception(f"artists not downloaded. Response: {r.text}")

print("Artists done")

# Download artist's albums ids. Includes all kinds of albums (albums, singles, etc.)
# This is necessary because when downloading albums via an artist api it doesn't download all info

albums_ids = []

for artist in artists_info:

    params = {
       'market':'CO' # For simplicity let's limit results to Colombia
    }

    r = requests.get(f"https://api.spotify.com/v1/artists/{artist['id']}/albums", params=params, headers=headers)

    if r.ok:
        ids = [album['id'] for album in r.json()['items']]
        albums_ids.extend(ids)
    else:
        raise Exception(f"{artist['name']} albums not downloaded. Response: {r.text}")

# Download album info & its track's ids

albums_info = []
tracks_ids = []

for album in albums_ids:
    params = {
       'market':'CO' # For simplicity let's limit results to Colombia
    }

    r = requests.get(f"https://api.spotify.com/v1/albums/{album}", params=params, headers=headers)

    if r.ok:
        albums_info.append(r.json())
    else:
        raise Exception(f"{album} not downloaded. Response: {r.text}")


    r = requests.get(f"https://api.spotify.com/v1/albums/{album}/tracks", params=params, headers=headers)

    if r.ok:
        ids = [track['id'] for track in r.json()['items']]
        tracks_ids.extend(ids)
    else:
        raise Exception(f"{album} tracks not downloaded. Response: {r.text}")

print("Albums done")

# Download Tracks

tracks_info = []

step = 50 # max number of tracks per request

for i in range(0, len(tracks_ids), step):
    params = {
        'ids':','.join(tracks_ids[i:i+step]),
        'market':'CO' # For simplicity let's limit results to Colombia
    }

    r = requests.get("https://api.spotify.com/v1/tracks", params=params, headers=headers)

    if r.ok:
        tracks_info.extend(r.json()['tracks'])
    else:
        raise Exception(f"tracks not downloaded. Response: {r.text}")

print("Tracks done")

# Download User
r = requests.get("https://api.spotify.com/v1/me", headers=headers)

if r.ok:
    user_info = r.json()
else:
    Exception(f"user not downloaded. Response: {r.text}")

print("User done")

# Download Playlists ids. This is necessary for the same reason as albums
# (Make sure the token has read private playlists scope!)

r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

if r.ok:
    playlists_ids = [playlist['id'] for playlist in r.json()['items']]
else:
    raise Exception(f"user's playlists ids not downloaded. Response: {r.text}")

# Download Playlists

playlist_info = []

for playlist in playlists_ids:
    params = {
       'market':'CO' # For simplicity let's limit results to Colombia
    }

    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist}", headers=headers)

    if r.ok:
        playlist_info.append(r.json())
    else:
        raise Exception(f"{playlist} playlist not downloaded. Response: {r.text}")

print("Playlists done")

# Save info

with open(f'{SAVE_PATH}/artists.json', 'w+') as f:
    f.write(json.dumps(artists_info, indent=4, sort_keys=True, ensure_ascii=False))

with open(f'{SAVE_PATH}/albums.json', 'w+') as f:
    f.write(json.dumps(albums_info, indent=4, sort_keys=True, ensure_ascii=False))

with open(f'{SAVE_PATH}/tracks.json', 'w+') as f:
    f.write(json.dumps(tracks_info, indent=4, sort_keys=True, ensure_ascii=False))

with open(f'{SAVE_PATH}/user.json', 'w+') as f:
    f.write(json.dumps(user_info, indent=4, sort_keys=True, ensure_ascii=False))

with open(f'{SAVE_PATH}/playlists.json', 'w+') as f:
    f.write(json.dumps(playlist_info, indent=4, sort_keys=True, ensure_ascii=False))

