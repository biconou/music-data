from flask import Flask, request, jsonify, Response
import discogs_client

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    d = discogs_client.Client(
        'my_user_agent/1.0',
        consumer_key='xxx',
        consumer_secret='xxx'
    )
    release = d.release(1293022)
    print(release)
    artists = release.artists
    #releases = d.search('iron maiden', type='artist')[0].releases
    #print(json(releases))
    return jsonify(artists)



if __name__ == '__main__':
    app.run(debug=True)
