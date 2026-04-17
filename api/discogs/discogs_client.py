#!/usr/bin/env python

import os

import discogs_client
import json

DISCOGS_KEY=os.getenv('DISCOGS_KEY')
DISCOGS_SECRET=os.getenv('DISCOGS_SECRET')

def main():
    d = discogs_client.Client(
        'my_user_agent/1.0',
        consumer_key=DISCOGS_KEY,
        consumer_secret=DISCOGS_SECRET
    )
    release = d.release(1293022)
    #print(json.dumps(release))
    print(release)
    artists = release.artists
    #releases = d.search('iron maiden', type='artist')[0].releases
    #print(json(releases))
    d.search('iron maiden', type='artist')[0].releases[0].artists

if __name__ == "__main__":
    main()