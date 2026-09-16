from flask import Flask, jsonify, request
from allmusic_routes import allmusic_bp, find_artist as find_allmusic_artist
from idagio_routes import idagio_bp
from masterdata_routes import masterdata_bp
from discogs.discogs import find_artist as find_discogs_artist
from discogs_routes import OUTPUT_DIR as DISCOGS_OUTPUT_DIR
from discogs_routes import discogs_bp, save_artist_to_json as save_discogs_artist
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(allmusic_bp)
app.register_blueprint(idagio_bp)
app.register_blueprint(masterdata_bp)
app.register_blueprint(discogs_bp)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/find-artist", methods=["GET"])
def find_artist():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    discogs_artist = find_discogs_artist(query)
    if discogs_artist:
        save_discogs_artist(discogs_artist["name"], discogs_artist, DISCOGS_OUTPUT_DIR)

    return find_allmusic_artist()


if __name__ == "__main__":
    app.run(debug=True)