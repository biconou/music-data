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
    artist['name'] = soup.select("h1#artistName")[0].contents[0].strip()
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
    # Parse and add biography data
    biography = parse_biography(artistId, htmlContent)
    artist['biography'] = biography
    return artist

# Biography
def parse_biography(artistId, htmlContent):
    try:
        soup = BeautifulSoup(htmlContent, 'html.parser')
        
        biography_data = {
            'id': artistId,
            'author': '',
            'text': '',
            'summary': ''
        }
        
        # Find the biography section
        biography_section = soup.select("div#biography.artistContentSubModule")
        
        if biography_section:
            biography_div = biography_section[0]
            
            # Extract author from the h3 tag
            h3_tag = biography_div.select("h3")[0]
            author_link = h3_tag.select("a.editorialAuthorLink")
            if author_link:
                biography_data['author'] = author_link[0].text.strip()
            
            # Extract biography text from all paragraphs
            paragraphs = biography_div.select("p")
            biography_text = []
            
            for para in paragraphs:
                # Get text from paragraph, clean it up
                para_text = para.get_text(separator=" ", strip=True)
                if para_text:
                    biography_text.append(para_text)
            
            # Join all paragraphs
            biography_data['text'] = "\n".join(biography_text)
            
            # Extract first paragraph as summary (usually most relevant)
            if biography_text:
                biography_data['summary'] = biography_text[0]
            
            logging.debug(f"Extracted biography for artist {artistId}: {len(biography_data['text'])} characters")
        else:
            logging.warning(f"Biography section not found for artist {artistId}")
        
        return biography_data
        
    except Exception as e:
        logging.error(f"Error parsing biography: {e}")
        return {
            'id': artistId,
            'author': '',
            'text': '',
            'summary': ''
        }

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
