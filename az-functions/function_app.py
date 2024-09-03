import azure.functions as func
import requests
import json
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="search-artist")
def search_artist(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get('query')
    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_allmusic_html_content(search_artist_url)
    artist = parse_search_artist(html_content)
    jsonArtist = json.dumps(artist, sort_keys=False, indent=4)
    return func.HttpResponse(jsonArtist,status_code=200)