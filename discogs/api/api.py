from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
import os
import discogs_client

load_dotenv()
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
d = discogs_client.Client(
    'my_user_agent/1.0',
    consumer_key= consumer_key,
    consumer_secret= consumer_secret
)
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    release = d.release(1293022)
    print("et voilà"+release)
    artists = release.artists
    #releases = d.search('iron maiden', type='artist')[0].releases
    #print(json(releases))
    return release



if __name__ == '__main__':
    app.run(debug=True)
