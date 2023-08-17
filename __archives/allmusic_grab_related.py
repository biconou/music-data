#!/usr/bin/env python
from fileinput import filename
import logging
from globals import *
from helpers import *


def grabRelated(artistId):
    logging.debug('Start grabRelated')
    logging.debug('Grab related html page for artist ' + artistId)
    relatedUrl = allmusicArtistBaseUrl + artistId + '/related'
    related = grabHTMLPage(relatedUrl)
    return related

def storeRelated(artistId):
    logging.debug('start storeDiscography')
    related = grabRelated(artistId)
    outputFileName = computeRelatedRawHTMLFileName(artistId)
    file = open(outputFileName, 'w')
    file.write('' + related)
    file.close()


def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    storeRelated('type-o-negative-mn0000206465')

if __name__ == '__main__':
    main()