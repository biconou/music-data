#!/usr/bin/env python
import os

rootDataDirectory = '../data'

allmusicArtistBaseUrl = 'https://www.allmusic.com/artist/'

rawHTMLFileNameSuffix = '.raw.html'

# Artist main page
def computeArtistRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/artist/' + artistId + rawHTMLFileNameSuffix

def computeArtistFileName(artistId):
    return os.path.abspath(rootDataDirectory + '/allmusic/artist/' + artistId + '.json')

# Discography
def computeRelatedRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/' + artistId + rawHTMLFileNameSuffix

def computeDiscographyFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/' + artistId

# Related
def computeRelatedRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId + rawHTMLFileNameSuffix

def computeRelatedFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId
