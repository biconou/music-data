#!/usr/bin/env python
import logging
from bs4 import BeautifulSoup
from globals import *


def parseArtistFromHtmlContent(artistId,htmlContent):

    soup = BeautifulSoup(htmlContent, 'html.parser')

    artist = {}
    artist['id'] = artistId

    artistName = soup.select("h1.artist-name")[0].string.strip()
    artist['name'] = artistName

    artist['basicInfo'] = str(soup.select("section.basic-info")[0].contents)
 
    artist['styles'] = []
    styles = soup.select("div.styles > div > a")
    for s in styles:
        logging.debug(s)
        styleName = s.string.strip()
        styleUrl = s['href']
        style = {
            'name' : styleName,
            'url' : styleUrl
            }
        artist['styles'].append(style)


    return artist
