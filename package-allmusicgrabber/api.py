from flask import Flask, request, jsonify, Response
import urllib.request
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content

app = Flask(__name__)

@app.route('/search-artist', methods=['GET'])
def receive_data():
    query = None
    # Try to get the JSON body
    if request.is_json:
        query = request.get_json().get('query')
        query = urllib.parse.quote(query)

    # If 'query' is None or not found in the JSON body, look for a query parameter in the URL
    if query is None:
        query = request.args.get('query')

    # If 'query' is still None, return an error response
    if query is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_allmusic_html_content(search_artist_url)
    artist = parse_search_artist(html_content)
    return jsonify(artist)

@app.route('/artist/<string:artist_id>', methods=['GET'])
def artist(artist_id):
    artist_url = compute_allmusic_artist_url(artist_id)
    html_content = fetch_allmusic_html_content(artist_url)
    artist = parse_artist(artist_id,html_content)
    return jsonify(artist)

@app.route('/discography/<string:artist_id>', methods=['GET'])
def discography(artist_id):
    discography_url = compute_allmusic_discography_url(artist_id)
    print(discography_url)
    html_content = fetch_allmusic_html_content(discography_url, referer=compute_allmusic_artist_url(artist_id))
    artist = parse_discography(artist_id,html_content)
    return jsonify(artist)

@app.route('/related/<string:artist_id>', methods=['GET'])
def related(artist_id):
    related_url = compute_allmusic_related_url(artist_id)
    print(related_url)
    html_content = fetch_allmusic_html_content(related_url, referer=compute_allmusic_artist_url(artist_id))
    artist = parse_related(artist_id,html_content)
    return jsonify(artist)

@app.route('/url-encode', methods=['POST'])
def url_encode():
    text = request.data.decode('utf-8')
    encoded_text = urllib.parse.quote(text)
    return Response(encoded_text, content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
