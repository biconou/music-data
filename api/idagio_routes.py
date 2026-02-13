from flask import Blueprint, request, jsonify
from idagiograbber.album import *
from dotenv import load_dotenv

load_dotenv()

idagio_bp = Blueprint("idagio", __name__, url_prefix="/idagio")

DATA_DIR = os.getenv("DATA_DIR")

@idagio_bp.route("/extract-album", methods=["POST"])
def extract_album():
    """
    Body JSON attendu :
    {
      "url": "https://app.idagio.com/fr/albums/archora-aion",
      "save_to_disk": true,           # optionnel
      "output_dir": "C:/chemin/...",  # optionnel
      "save_html": false              # optionnel
    }
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "Champ 'url' requis dans le JSON d'entrée"}), 400

    save_to_disk = data.get("save_to_disk", False)
    save_html = data.get("save_html", False)
    output_dir = data.get("output_dir") if save_to_disk else None

    if save_to_disk and not output_dir:
        output_dir = os.path.join(DATA_DIR, "idagio","album")

    try:
        result = scrape_idagio_album(
            url,
            output_dir=output_dir,
            save_html=save_html
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500