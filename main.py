from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    # Base64 encode the client ID and client secret
    auth_string = client_id + ':' + client_secret
    base64_auth_creds = base64.b64encode(auth_string.encode())

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": f"Basic {base64_auth_creds.decode()}"
    }

    data = {
        "grant_type": "client_credentials"}

    # Request access token
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    # Extract the access token
    token = response_data['access_token']
    return token


def search_for_artist(token, artist_name):
    endpoint = 'https://api.spotify.com/v1/search'
    headers = {
        "Authorization": f"Bearer {token}",
    }
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }

    response = requests.get(endpoint, headers=headers, params=params)
    json_response = json.loads(response.content)['artists']['items']
    if response.status_code == 200:
        if len(json_response) == 0:
            print('No artist with this name found')
        else:
            return json_response[0]
    else:
        print("Error searching for artist")


def top_tracks_by_artist(token, artist_id):
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        'market': 'US'
    }

    response = requests.get(endpoint, headers=headers, params=params)
    json_response = json.loads(response.content)['tracks']
    return json_response


token = get_token()
result = search_for_artist(token, 'Led Zeppelin')
id = result['id']
songs = top_tracks_by_artist(token, id)

# for i, song in enumerate(songs):
#   print(f"{i + 1}. {song['name']}")

tracks = []
for i, song in enumerate(songs):
    track = (f"{i + 1}. {song['name']}")
    tracks.append(track)

print(tracks)
