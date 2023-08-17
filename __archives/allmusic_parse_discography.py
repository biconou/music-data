#!/usr/bin/env python
import logging
from bs4 import BeautifulSoup
from globals import *
import json


def readDiscographyFromFile(artistId):
    logging.debug('start readDiscographyFromFile')
    discographyFileName = computeRelatedRawHTMLFileName(artistId)
    logging.debug('discographyFileName : ' + discographyFileName)
    discography = open(discographyFileName, 'r').read()
    return discography

def parseDicography(artistId):
    logging.debug("start parse")

    html = readDiscographyFromFile(artistId)
    soup = BeautifulSoup(html, 'html.parser')

    discographyList = soup.select("section.discography > table > tbody > tr")
    list = []
    for u in discographyList:
        albumYear = u.select("td.year")[0].string.strip()
        logging.debug(albumYear)
        albumTitle = u.select("td.title")[0]['data-sort-value']
        logging.debug(albumTitle)
        list.append({'albumYear': albumYear, 'albumTitle': albumTitle})
    return list

def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    artistId = 'celtic-frost-mn0000191063'

    disco = parseDicography(artistId)
    artist = {
        'id': artistId,
        'albums': disco
    }

    with open(computeDiscographyFileName(artistId), 'w') as f:
        f.write(json.dumps(artist, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()