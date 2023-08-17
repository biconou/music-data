#!/usr/bin/env python
import logging
from bs4 import BeautifulSoup
from globals import *
import json


def readRelatedFromFile(artistId):
    logging.debug('start readRelatedFromFile')
    relatedFileName = computeRelatedRawHTMLFileName(artistId)
    logging.debug('relatedFileName : ' + relatedFileName)
    related = open(relatedFileName, 'r').read()
    return related

def parseRelated(artistId):
    logging.debug("start parse")

    html = readRelatedFromFile(artistId)
    soup = BeautifulSoup(html, 'html.parser')

    similarList = soup.select('section.related.similars > ul > li >a')
    list = []
    for u in similarList:
        similarArtist = u.string
        list.append(similarArtist)
    return list

def main():
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    artistId = 'type-o-negative-mn0000206465'

    related = parseRelated(artistId)
    artist = {
        'id': artistId,
        'related': {'similars': related}
    }

    with open(computeRelatedFileName(artistId), 'w') as f:
        f.write(json.dumps(artist, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()