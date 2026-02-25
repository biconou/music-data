from genericpath import exists

import requests
import json
import os

STRAPI_URL = os.getenv("STRAPI_URL")

def check_artist_id(artist_id):
    url = f"{STRAPI_URL}/api/artists?filters%5Ballmusic_id%5D={artist_id}"
    
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")
    try:
        data = resp.json()
    except json.JSONDecodeError:
        data = json.loads(resp.text)

    allmusic_ids = [
        item["id"]
        for item in data["data"]
        if item.get("id") is not None
    ]

    return allmusic_ids

def get_artist_by_allmusic_id(artist_id):
    ids = check_artist_id(artist_id)
    if ids:
        found_id =ids[0]
        url = f"{STRAPI_URL}/api/artists/{found_id}"
        resp = requests.get(url)
        return resp.json()

def generate_artist_data(allmusic_json):
    allmusic_data = allmusic_json
    if allmusic_json.get("data") is not None:
        allmusic_data = allmusic_json["data"]
    return {
        "data": {
            "allmusic_id": allmusic_data.get("allmusic_id"),
            "name": allmusic_data.get("name"),
            "discography": allmusic_data.get("discography"),
            "allmusic_data": allmusic_data
        }
    }

def create_or_update_artist(any_json):
    artistId = any_json.get("allmusic_id")
    if any_json.get("data") is not None:
        artistId = any_json.get("data").get("allmusic_id")        
    existing_ids = check_artist_id(artistId)
    if existing_ids:
        return update_artist(existing_ids[0], any_json)
    else:
        return create_artist(any_json)

def create_artist(any_json):
    url = f"{STRAPI_URL}/api/artists"
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, data=json.dumps(generate_artist_data(any_json)))
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")
    return resp.json()

def update_artist(artistId,any_json):
    url = f"{STRAPI_URL}/api/artists/{artistId}"
    headers = {"Content-Type": "application/json"}
    resp = requests.put(url, headers=headers, data=json.dumps(generate_artist_data(any_json)))
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")
    return resp.json()
