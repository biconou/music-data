import azure.functions as func
import requests
import json
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="search-artist")
def search_artist(req: func.HttpRequest) -> func.HttpResponse:
    query = None
    try:
        # Check if the request has a JSON body
        if req.get_json():
            req_body = req.get_json()
            query = req_body.get('query')
    except ValueError:
        pass  # JSON decoding failed
    # Fallback to query parameters if no JSON body or `query` is missing
    if query is None:
        query = req.params.get('query')
    if query is None:
        return func.HttpResponse(
            json.dumps({'error': 'Query parameter is missing'}),
            status_code=400,
            mimetype="application/json"
        )
    try:
        search_artist_url = compute_allmusic_search_artist_url(query)
        html_content = fetch_allmusic_html_content(search_artist_url)
        artist = parse_search_artist(html_content)
        jsonArtist = json.dumps(artist, sort_keys=False, indent=4)
        return func.HttpResponse(jsonArtist,status_code=200)
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=400,
            mimetype="application/json"
        )
    

