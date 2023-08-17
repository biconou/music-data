#!/usr/bin/env python
from fileinput import filename
import logging
import subprocess
import sys
from globals import *
from helpers import *


def grabDiscography(artistId):
    logging.debug('Start grabDiscography')
    logging.debug('Grab discography html page for artist ' + artistId)
    discographyUrl = allmusicArtistBaseUrl + artistId + '/discography'
    discography = grabHTMLPage(discographyUrl)
    return discography

def storeDiscography(artistId):
    logging.debug('start storeDiscography')
    discography = grabDiscography(artistId)
    outputFileName = computeRelatedRawHTMLFileName(artistId)
    file = open(outputFileName, 'w')
    file.write('' + discography)
    file.close()


def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    storeDiscography('celtic-frost-mn0000191063')

if __name__ == '__main__':
    main()