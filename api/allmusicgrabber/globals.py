#!/usr/bin/env python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

rootDataDirectory = '../data'
allmusicArtistBaseUrl = 'https://www.allmusic.com/artist/'
rawHTMLFileNameSuffix = '.xml'

# Lecture de la variable d'environnement pour verify
# Valeurs acceptées : "true", "1", "false", "0" (insensibles à la casse)
verify_env = os.getenv("VERIFY_SSL", "false").lower()
VERIFY_SSL = verify_env in ["true", "1", "yes", "y"]

# Artist main page
def computeArtistRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/artist/HTML/' + artistId + rawHTMLFileNameSuffix

def computeArtistFileName(artistId):
    return os.path.abspath(rootDataDirectory + '/allmusic/artist/' + artistId + '.json')

# Discography
def computeDiscographyRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/HTML/' + artistId + rawHTMLFileNameSuffix

def computeDiscographyFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/' + artistId

# Related
def computeRelatedRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId + rawHTMLFileNameSuffix

def computeRelatedFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId


def fetch_allmusic_html_content(url,referer=None):
    try:
        headers={"Accept" : '*/*',
                 "Host" : "www.allmusic.com",
                 "user-agent" : "curl/7.88.1",
                 "referer" : "url"}
        if referer is not None:
            headers['referer'] = referer

        response = requests.get(url,headers=headers,verify=VERIFY_SSL)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Une erreur s'est produite dans fetch : {e}")
        return None
