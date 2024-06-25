from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
from urllib.parse import quote_plus,unquote
from allmusicgrabber.artist import *

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


@app.route('/search-artist', methods=['GET'])
def search_artist():
    query = request.args.get('query')
    search_artist_url = compute_allmusic_search_artist_url(query)
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
    artist = parse_discography(artist_id,html_content)
    return jsonify(artist)

@app.route('/related/<string:artist_id>', methods=['GET'])
def related(artist_id):
    related_url = compute_allmusic_related_url(artist_id)
    print(related_url)
    html_content = fetch_html_content(related_url, referer=compute_allmusic_artist_url(artist_id))
    artist = parse_related(artist_id,html_content)
    return jsonify(artist)

if __name__ == '__main__':
    app.run(debug=True)
