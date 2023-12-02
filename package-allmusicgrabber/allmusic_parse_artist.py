#!/usr/bin/env python
import logging
from allmusicgrabber.globals import *
from allmusicgrabber.artist import *
import json


def readArtistFromFile(artistId):
    artistFileName = computeArtistRawHTMLFileName(artistId)
    artist = open(artistFileName, 'r').read()
    return artist

def parseArtist(artistId):
    html = readArtistFromFile(artistId)
    artist = parseArtistFromHtmlContent(artistId, html)
    return artist

def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    artistId = 'celtic-frost-mn0000191063'
    artist = parseArtist(artistId)
    with open(computeArtistFileName(artistId), 'w') as f:
        f.write(json.dumps(artist, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()