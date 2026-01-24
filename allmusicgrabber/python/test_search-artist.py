#!/usr/bin/env python
from allmusicgrabber.artist import *
from allmusicgrabber.globals import fetch_allmusic_html_content
import json

def main():
    print("debut")
    query = 'dismember'
    search_artist_url = compute_allmusic_search_artist_url(query)
    html_content = fetch_allmusic_html_content(search_artist_url)
    foundArtist = parse_search_artist(html_content)
    artistId = foundArtist['artistId']
    #
    artist_url = compute_allmusic_artist_url(artistId)
    html_content = fetch_allmusic_html_content(artist_url)
    artist = parse_artist(artistId, html_content)
    #
    discography_url = compute_allmusic_discography_url(artistId)
    html_content = fetch_allmusic_html_content(discography_url)
    discography = parse_discography(artistId, html_content)
    #
    related_url = compute_allmusic_related_url(artistId)
    html_content = fetch_allmusic_html_content(related_url)
    related = parse_related(artistId, html_content)

    #artist.update(discography)

    print(artist)

if __name__ == "__main__":
    main()