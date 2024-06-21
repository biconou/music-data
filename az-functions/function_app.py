import azure.functions as func
from urllib.parse import quote_plus,unquote
import logging
import requests
from bs4 import BeautifulSoup
import re
import json

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

# search-artist
def compute_allmusic_search_artist_url(query):
    return "https://www.allmusic.com/search/artists/" + quote_plus(query)

def parse_search_artist(html_content):
    try :
        soup = BeautifulSoup(html_content, 'html.parser')
        artist = {}
        print(soup.select("div.artist"))
        artistNode=soup.select("div.artist")[0]
        artist['name'] = artistNode.select("div.info > div.name a")[0].text.strip()
        artist['url'] = artistNode.select("div.info > div.name a")[0]["href"]
        artist['artistId']=unquote(re.sub(r".*/artist/","",artist['url']))
        artist['genres'] = artistNode.select("div.info > div.genres")[0].text.strip()
        artist['decades'] = artistNode.select("div.info > div.decades")[0].text.strip()
        return artist
    except Exception as e:
        print(f"Une erreur s'est produite dans parse : {e}")
        return None

@app.route(route="search_artist")
def search_artist(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    search_artist_url = ""
    jsonArtist = ""
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
    else:
        search_artist_url = compute_allmusic_search_artist_url(query)
        html_content = fetch_html_content(search_artist_url)
        artist = parse_search_artist(html_content)
        jsonArtist = json.dumps(artist, sort_keys=False, indent=4)

    return func.HttpResponse(jsonArtist,status_code=200)