from flask import Blueprint, request, jsonify
from idagiograbber.album import *
from dotenv import load_dotenv

load_dotenv()

idagio_bp = Blueprint("idagio", __name__, url_prefix="/idagio")

def str_to_bool(s: str, *, default=False) -> bool:
    if s is None:
        return default
    v = s.strip().lower()
    if v in {"1", "true", "yes", "y", "on", "oui", "o"}:
        return True
    if v in {"0", "false", "no", "n", "off", "non", ""}:
        return False
    raise ValueError(f"VERIFY_SSL invalide: {s!r}")

VERIFY_SSL = str_to_bool(os.getenv("VERIFY_SSL"), default=True)
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