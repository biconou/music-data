from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
from urllib.parse import quote_plus,unquote
from allmusicgrabber.artist import parseDiscographyFromHtmlContent, parseRelatedFromHtmlContent

app = Flask(__name__)

def write_to_file(filename, text_content):
    try:
        # Ouvrir le fichier en mode écriture (écrase le fichier s'il existe)
        with open(filename, 'w', encoding='utf-8') as file:
            # Écrire le contenu texte dans le fichier
            file.write(text_content)
        print(f"Le contenu a été écrit avec succès dans le fichier '{filename}'.")
    except IOError as e:
        print(f"Une erreur s'est produite lors de l'écriture dans le fichier : {e}")

def compute_allmusic_search_artist_url(query):
    return "https://www.allmusic.com/search/artists/" + quote_plus(query)

def compute_allmusic_artist_url(artist_id):
    return "https://www.allmusic.com/artist/" + artist_id

def compute_allmusic_discography_url(artist_id):
    return "https://www.allmusic.com/artist/%s/discographyAjax" % (artist_id)

def compute_allmusic_related_url(artist_id):
    return "https://www.allmusic.com/artist/%s/relatedArtistsAjax" % (artist_id)

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
    
def parse_artist(artistId,htmlContent):
    soup = BeautifulSoup(htmlContent, 'html.parser')
    artist = {'id':artistId}
    artist['name'] = soup.select("h1#artistName")[0].string.strip()
    artist['activeDates'] = str(soup.select("#basicInfoMeta > div.activeDates > div")[0].text)
    artistBirth = soup.select("#basicInfoMeta > div.birth > div > a")
    artist['birthDate'] = str(artistBirth[0].text) if len(artistBirth) > 0 else ""
    artist['birthPlace'] = str(artistBirth[1].text) if len(artistBirth) > 1 else ""
    artist['styles'] = []
    styles = soup.select("div.styles > div > a")
    for s in styles:
        styleName = s.string.strip()
        styleUrl = s['href']
        style = {
            'name' : styleName,
            'url' : styleUrl
            }
        artist['styles'].append(style)
    return artist

@app.route('/search-artist', methods=['GET'])
def search_artist():
    query = request.args.get('query')
    search_artist_url = compute_allmusic_search_artist_url(query)
    print(search_artist_url)
    html_content = fetch_html_content(search_artist_url)
    artist = parse_search_artist(html_content)
    return jsonify(artist)

@app.route('/artist/<string:artist_id>', methods=['GET'])
def artist(artist_id):
    artist_url = compute_allmusic_artist_url(artist_id)
    html_content = fetch_html_content(artist_url)
    artist = parse_artist(artist_id,html_content)
    return jsonify(artist)

@app.route('/discography/<string:artist_id>', methods=['GET'])
def discography(artist_id):
    discography_url = compute_allmusic_discography_url(artist_id)
    print(discography_url)
    html_content = fetch_html_content(discography_url, referer=compute_allmusic_artist_url(artist_id))
    artist = parseDiscographyFromHtmlContent(artist_id,html_content)
    return jsonify(artist)

@app.route('/related/<string:artist_id>', methods=['GET'])
def related(artist_id):
    related_url = compute_allmusic_related_url(artist_id)
    print(related_url)
    html_content = fetch_html_content(related_url, referer=compute_allmusic_artist_url(artist_id))
    artist = parseRelatedFromHtmlContent(artist_id,html_content)
    return jsonify(artist)

if __name__ == '__main__':
    app.run(debug=True)
