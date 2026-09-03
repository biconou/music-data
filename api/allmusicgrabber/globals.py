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
        headers={"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                 "Host" : "www.allmusic.com",
                 "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                 "Accept-Language": "en-US,en;q=0.5"}
        if referer is not None:
            headers['referer'] = referer
        else:
            headers['referer'] = "https://www.allmusic.com/"

        response = requests.get(url,headers=headers,verify=VERIFY_SSL)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Une erreur s'est produite dans fetch : {e}")
        return None
