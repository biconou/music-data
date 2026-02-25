from flask import Blueprint, request, jsonify
from idagiograbber.album import *
from dotenv import load_dotenv
from masterdata.artist import get_artist_by_allmusic_id
from masterdata.artist import update_artist as update_artist_func
from masterdata.artist import create_or_update_artist as create_or_update_artist_func

load_dotenv()

masterdata_bp = Blueprint("masterdata", __name__, url_prefix="/masterdata")

VERIFY_SSL = os.getenv("VERIFY_SSL")
DATA_DIR = os.getenv("DATA_DIR")

@masterdata_bp.route("/artist", methods=["GET"])
def get_artist():
    artist_id = request.args.get("artist_id")
    if not artist_id:
        return jsonify({"error": "Query parameter 'artist_id' is required"}), 400

    try:
        result = get_artist_by_allmusic_id(artist_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@masterdata_bp.route("/artist", methods=["POST"])    
def create_or_update_artist():
    data = request.get_json()
    try:
        result = create_or_update_artist_func(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@masterdata_bp.route("/artist/<artistId>", methods=["PUT"])
def update_artist(artistId):
    data = request.get_json()
    try:
        result = update_artist_func(artistId, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500