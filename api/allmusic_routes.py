from flask import Blueprint, request, jsonify
import urllib
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

allmusic_bp = Blueprint("allmusic", __name__, url_prefix="/allmusic")

DATA_DIR = os.getenv("DATA_DIR")
OUTPUT_DIR = os.path.join(DATA_DIR, "allmusic","artists")

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


@allmusic_bp.route('/find-artist', methods=['GET'])
def find_artist():
    query = None
    if request.is_json:
        body = request.get_json()
        if body:
            query = body.get('query')
            if query:
                query = urllib.parse.quote(query)

    if query is None:
        query = request.args.get('query')

    if query is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_allmusic_html_content(search_artist_url)
    foundArtist = parse_search_artist(html_content)
    artistId = foundArtist['artistId']

    artist_url = compute_allmusic_artist_url(artistId)
    html_content = fetch_allmusic_html_content(artist_url)
    artist = parse_artist(artistId, html_content)

    discography_url = compute_allmusic_discography_url(artistId)
    html_content = fetch_allmusic_html_content(
        discography_url,
        referer=compute_allmusic_artist_url(artistId)
    )
    discography = parse_discography(artistId, html_content)

    related_url = compute_allmusic_related_url(artistId)
    html_content = fetch_allmusic_html_content(
        related_url,
        referer=compute_allmusic_artist_url(artistId)
    )
    related = parse_related(artistId, html_content)

    artist.update(discography)
    artist.update(related)

    save_artist_to_json(artistId, artist, OUTPUT_DIR)

    return jsonify(artist)


@allmusic_bp.route('/search-artist', methods=['GET'])
def search_artist():
    query = None
    if request.is_json:
        body = request.get_json()
        if body:
            query = body.get('query')
            if query:
                query = urllib.parse.quote(query)

    if query is None:
        query = request.args.get('query')

    if query is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_allmusic_html_content(search_artist_url)
    artist = parse_search_artist(html_content)
    return jsonify(artist)


@allmusic_bp.route('/artist/<string:artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist_url = compute_allmusic_artist_url(artist_id)
    html_content = fetch_allmusic_html_content(artist_url)
    artist = parse_artist(artist_id, html_content)
    return jsonify(artist)


@allmusic_bp.route('/discography/<string:artist_id>', methods=['GET'])
def get_discography(artist_id):
    discography_url = compute_allmusic_discography_url(artist_id)
    html_content = fetch_allmusic_html_content(
        discography_url,
        referer=compute_allmusic_artist_url(artist_id)
    )
    discography = parse_discography(artist_id, html_content)
    return jsonify(discography)


@allmusic_bp.route('/related/<string:artist_id>', methods=['GET'])
def get_related(artist_id):
    related_url = compute_allmusic_related_url(artist_id)
    html_content = fetch_allmusic_html_content(
        related_url,
        referer=compute_allmusic_artist_url(artist_id)
    )
    related = parse_related(artist_id, html_content)
    return jsonify(related)