#!/usr/bin/env python

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import discogs_client
import json
from env_utils import load_api_env

VERIFY_SSL, DISCOGS_KEY, DISCOGS_SECRET, _ = load_api_env()

def main():
    d = discogs_client.Client(
        consumer_key=DISCOGS_KEY,
        consumer_secret=DISCOGS_SECRET,
        user_agent='MyDiscogsApp/1.0 +https://example.com'
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