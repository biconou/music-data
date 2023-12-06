#!/usr/bin/env python

import discogs_client
import json

def main():
    d = discogs_client.Client(
        'my_user_agent/1.0',
        consumer_key='BIqHCSNxDnaIPhqCiZoc',
        consumer_secret='xYpdaTwFFISNXwMOlvuGVossTaRtnkHs'
    )
    release = d.release(1293022)
    #print(json.dumps(release))
    print(release)
    artists = release.artists
    #releases = d.search('iron maiden', type='artist')[0].releases
    #print(json(releases))


if __name__ == "__main__":
    main()