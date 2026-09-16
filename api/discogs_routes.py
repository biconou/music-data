from flask import Blueprint, Flask, request, jsonify, Response
from discogs.discogs import search as discogs_search
import os
import json
from env_utils import load_api_env
from datetime import datetime

discogs_bp = Blueprint("discogs", __name__, url_prefix="/discogs")
_, _, _, DATA_DIR = load_api_env()

OUTPUT_DIR = os.path.join(DATA_DIR, "discogs","artists")

def save_artist_to_json(artist_id: str, artist_data: dict, base_dir: str):
    os.makedirs(base_dir, exist_ok=True)

    file_path = os.path.join(base_dir, f"{artist_id}.json")

    payload = {
        "artistId": artist_id,
        "fetchedAt": datetime.utcnow().isoformat() + "Z",
        "data": artist_data
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def find_artist():
    artist_name = request.args.get("q", "")
    if not artist_name:
        return jsonify({"error": "Missing artist name"}), 400

    from discogs.discogs import find_artist as discogs_find_artist
    artist = discogs_find_artist(artist_name)
    return artist


@discogs_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    search_type = request.args.get("type", None)
    per_page = int(request.args.get("per_page", 10))
    page = int(request.args.get("page", 1))
    filters = {k: v for k, v in request.args.items() if k not in ("q", "type", "per_page", "page")}

    data = discogs_search(query, search_type=search_type, per_page=per_page, page=page, **filters)
    return jsonify(data), 200


@discogs_bp.route("/find-artist", methods=["GET"])
def find_artist_route():
    artist = find_artist()
    if artist:
        save_artist_to_json(artist["name"], artist, OUTPUT_DIR)
        return jsonify(artist), 200
    return jsonify({"error": "Artist not found"}), 404


