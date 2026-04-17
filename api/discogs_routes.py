from flask import Blueprint, Flask, request, jsonify, Response
from discogs.discogs import search as discogs_search

discogs_bp = Blueprint("discogs", __name__, url_prefix="/discogs")

@discogs_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    search_type = request.args.get("type", None)
    per_page = int(request.args.get("per_page", 10))
    page = int(request.args.get("page", 1))
    filters = {k: v for k, v in request.args.items() if k not in ("q", "type", "per_page", "page")}

    data = discogs_search(query, search_type=search_type, per_page=per_page, page=page, **filters)
    return jsonify(data), 200



