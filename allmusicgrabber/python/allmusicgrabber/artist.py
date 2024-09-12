#!/usr/bin/env python
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, unquote
import re

# Artist search
def compute_allmusic_search_artist_url(query):
    return "https://www.allmusic.com/search/artists/" + quote_plus(query)

def parse_search_artist(html_content):
    try :
        soup = BeautifulSoup(html_content, 'html.parser')
        artist = {}
        print(soup.select("div.artist"))
        artistNode=soup.select("div.artist")[0]
        artist['name'] = artistNode.select("div.info > div.name a")[0].text.strip()
        artist['url'] = artistNode.select("div.info > div.name a")[0]["href"]
        artist['artistId']=unquote(re.sub(r".*/artist/","",artist['url']))
        artist['genres'] = artistNode.select("div.info > div.genres")[0].text.strip()
        artist['decades'] = artistNode.select("div.info > div.decades")[0].text.strip()
        return artist
    except Exception as e:
        print(f"Une erreur s'est produite dans parse : {e}")
        return None

# Artist
def compute_allmusic_artist_url(artist_id):
    return "https://www.allmusic.com/artist/" + artist_id

def parse_artist(artistId,htmlContent):
    soup = BeautifulSoup(htmlContent, 'html.parser')
    artist = {'allmusic_id':artistId}
    artist['name'] = soup.select("h1#artistName")[0].string.strip()
    artist['activeDates'] = str(soup.select("#basicInfoMeta > div.activeDates > div")[0].text)
    artistBirth = soup.select("#basicInfoMeta > div.birth > div > a")
    artist['birthDate'] = str(artistBirth[0].text) if len(artistBirth) > 0 else ""
    artist['birthPlace'] = str(artistBirth[1].text) if len(artistBirth) > 1 else ""
    artist['styles'] = []
    styles = soup.select("div.styles > div > a")
    for s in styles:
        styleName = s.string.strip()
        styleUrl = s['href']
        style = {
            'name' : styleName,
            'url' : styleUrl
            }
        artist['styles'].append(style)
    return artist

# Discography
def compute_allmusic_discography_url(artist_id):
    return "https://www.allmusic.com/artist/%s/discographyAjax" % (artist_id)

def parse_discography(artistId,htmlContent):

    soup = BeautifulSoup(htmlContent, 'html.parser')

    artist = {}
    artist['id'] = artistId

    discographyList = soup.select("#discographyResults > table > tbody > tr")
    list = []
    for u in discographyList:
        # Year
        albumYear = u.select("td.year")[0].string
        if (albumYear) != None :
            albumYear = albumYear.strip()
        logging.debug(albumYear)
        # Title
        albumTitle = u.select("td.meta")[0]['data-text']
        logging.debug(albumTitle)
        # Ratings
        musicRating = u.select("td.musicRating")[0]['data-text']
        avgRating = u.select("td.avgRating")[0]['data-text']
        #
        list.append({'albumYear': albumYear, 'albumTitle': albumTitle, 'musicRating': musicRating, 'avgRating': avgRating})
    artist['discography'] = list

    return artist

# Related
def compute_allmusic_related_url(artist_id):
    return "https://www.allmusic.com/artist/%s/relatedArtistsAjax" % (artist_id)

def parse_related(artistId,htmlContent):

    soup = BeautifulSoup(htmlContent, 'html.parser')

    artist = {}
    artist['id'] = artistId
    artist['related'] = {}
    # Similars
    similarsList = soup.select("div.similars > a")
    list = []
    for u in similarsList:
        list.append({'artist': u['title'], 'ArtistId': u['href'].replace("/artist/","")})
    artist['related']['similars'] = list
    # influencers
    influencersList = soup.select("div.influencers > a")
    list = []
    for u in influencersList:
        list.append({'artist': u['title'], 'ArtistId': u['href'].replace("/artist/","")})
    artist['related']['influencers'] = list
    # followers
    followersList = soup.select("div.followers > a")
    list = []
    for u in followersList:
        list.append({'artist': u['title'], 'ArtistId': u['href'].replace("/artist/","")})
    artist['related']['followers'] = list
    # associatedwith
    associatedwithList = soup.select("div.associatedwith > a")
    list = []
    for u in associatedwithList:
        list.append({'artist': u['title'], 'ArtistId': u['href'].replace("/artist/","")})
    artist['related']['associatedwith'] = list

    return artist
