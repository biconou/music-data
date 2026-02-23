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

def generate_artist_data(any_json):
    if any_json.get("data") is not None:
        any_json = any_json["data"]
    return {
        "data": {
            "allmusic_id": any_json.get("allmusic_id"),
            "name": any_json.get("name")
        }
    }

def create_artist(data):
    url = f"{STRAPI_URL}/api/artists"
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, data=json.dumps(generate_artist_data(data)))
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")
    return resp.json()
