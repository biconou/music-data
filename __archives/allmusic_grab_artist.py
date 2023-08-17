#!/usr/bin/env python
import logging
from globals import *
from helpers import *


def grabArtist(artistId):
    logging.debug('Grab artist html page for artist ' + artistId)
    artistUrl = allmusicArtistBaseUrl + artistId
    artist = grabHTMLPage(artistUrl)
    return artist

def storeArtist(artistId):
    logging.debug('start storeArtist')
    artist = grabArtist(artistId)
    outputFileName = computeArtistRawHTMLFileName(artistId)
    file = open(outputFileName, 'w')
    file.write('' + artist)
    file.close()


def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    storeArtist('type-o-negative-mn0000206465')

if __name__ == '__main__':
    main()