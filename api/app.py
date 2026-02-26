from flask import Flask, jsonify
from allmusic_routes import allmusic_bp
from idagio_routes import idagio_bp
from masterdata_routes import masterdata_bp
from discogs_routes import discogs_bp
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


if __name__ == "__main__":
    app.run(debug=True)