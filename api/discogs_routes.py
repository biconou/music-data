from flask import Blueprint, Flask, request, jsonify, Response
from dotenv import load_dotenv
import os
import discogs_client

load_dotenv()

discogs_bp = Blueprint("discogs", __name__, url_prefix="/discogs")

consumer_key = os.getenv("DISCOGS_KEY")
consumer_secret = os.getenv("DISCOGS_SECRET")

d = discogs_client.Client(
    'my_user_agent/1.0',
    consumer_key= consumer_key,
    consumer_secret= consumer_secret
)

@discogs_bp.route("/search", methods=["GET"])
def search():
    release = d.release(1293022)
    #releases = d.search('iron maiden', type='artist')[0].releases
    #print(json(releases))
    return jsonify(release.data), 200



