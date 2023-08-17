#!/usr/bin/env python
import logging
from bs4 import BeautifulSoup


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

def parseDiscographyFromHtmlContent(artistId,htmlContent):

    soup = BeautifulSoup(htmlContent, 'html.parser')

    artist = {}
    artist['id'] = artistId

    discographyList = soup.select("section.discography > table > tbody > tr")
    list = []
    for u in discographyList:
        albumYear = u.select("td.year")[0].string.strip()
        logging.debug(albumYear)
        albumTitle = u.select("td.title")[0]['data-sort-value']
        logging.debug(albumTitle)
        list.append({'albumYear': albumYear, 'albumTitle': albumTitle})
    artist['discography'] = list

    return artist
