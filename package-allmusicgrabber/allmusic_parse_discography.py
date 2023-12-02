#!/usr/bin/env python
import logging
from allmusicgrabber.globals import *
from allmusicgrabber.artist import *
import json


def readDiscographyFromFile(artistId):
    discographyFileName = computeDiscographyRawHTMLFileName(artistId)
    discography = open(discographyFileName, 'r').read()
    return discography

def parseDiscography(artistId):
    html = readDiscographyFromFile(artistId)
    discography = parseDiscographyFromHtmlContent(artistId, html)
    return discography

def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    artistId = 'celtic-frost-mn0000191063'
    artist = parseDiscography(artistId)
    print(json.dumps(artist, sort_keys=False, indent=4))
  #  with open(computeArtistFileName(artistId), 'w') as f:
  #      f.write(json.dumps(artist, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()