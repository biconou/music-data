from flask import Flask, jsonify
from allmusic_routes import allmusic_bp
from idagio_routes import idagio_bp

app = Flask(__name__)

app.register_blueprint(allmusic_bp)
app.register_blueprint(idagio_bp)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)