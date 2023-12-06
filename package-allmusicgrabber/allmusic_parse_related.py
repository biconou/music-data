#!/usr/bin/env python
import logging
from allmusicgrabber.globals import *
from allmusicgrabber.artist import *
import json


def readRelatedFromFile(artistId):
    relatedFileName = computeRelatedRawHTMLFileName(artistId)
    related = open(relatedFileName, 'r').read()
    return related

def parseRelated(artistId):
    html = readRelatedFromFile(artistId)
    related = parseRelatedFromHtmlContent(artistId, html)
    return related

def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    artistId = 'celtic-frost-mn0000191063'
    related = parseRelated(artistId)
    print(json.dumps(related, sort_keys=False, indent=4))
  #  with open(computeArtistFileName(artistId), 'w') as f:
  #      f.write(json.dumps(artist, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()