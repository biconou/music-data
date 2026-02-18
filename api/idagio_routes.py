from flask import Blueprint, request, jsonify
from idagiograbber.album import *
from dotenv import load_dotenv

load_dotenv()

idagio_bp = Blueprint("idagio", __name__, url_prefix="/idagio")

VERIFY_SSL = os.getenv("VERIFY_SSL")
DATA_DIR = os.getenv("DATA_DIR")
OUTPUT_DIR = os.path.join(DATA_DIR, "idagio","album")

@idagio_bp.route("/extract-album", methods=["GET"])
def extract_album():
    """
    Expects a query parameter:
      /extract-album?album=<album_url_or_id>
    """
    album = request.args.get("album")
    if not album:
        return jsonify({"error": "Query parameter 'album' is required"}), 400

    try:
        result = download_html_album_data_from_api(album, OUTPUT_DIR,VERIFY_SSL)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500