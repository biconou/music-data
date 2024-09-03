import azure.functions as func
from urllib.parse import quote_plus,unquote
import requests
import json
from allmusicgrabber.artist import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def fetch_html_content(url,referer=None):
    try:
        headers={"Accept" : '*/*',
                 "Host" : "www.allmusic.com",
                 "user-agent" : "curl/7.88.1",
                 "referer" : "url"}
        if referer is not None:
            headers['referer'] = referer
        
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Une erreur s'est produite dans fetch : {e}")
        return None


@app.route(route="search_artist")
def search_artist(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get('query')
    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_html_content(search_artist_url)
    artist = parse_search_artist(html_content)
    jsonArtist = json.dumps(artist, sort_keys=False, indent=4)
    return func.HttpResponse(jsonArtist,status_code=200)