import os
from flask import Flask, request, jsonify, Response, redirect, url_for, session
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)

azure = oauth.remote_app(
    'azure',
    consumer_key=os.getenv('AZURE_CLIENT_ID'),
    consumer_secret=os.getenv('AZURE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'User.Read',
        'response_type': 'code'
    },
    base_url='https://graph.microsoft.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f"{os.getenv('AZURE_AUTHORITY')}/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token",
    authorize_url=f"{os.getenv('AZURE_AUTHORITY')}/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/authorize"
)

@app.route('/login')
def login():
    return azure.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('oauth_token')
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    response = azure.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error'], request.args['error_description']
        )
    session['oauth_token'] = (response['access_token'], '')
    return 'You are logged in!'

@azure.tokengetter
def get_azure_oauth_token():
    return session.get('oauth_token')


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


if __name__ == '__main__':
    app.run(debug=True)
