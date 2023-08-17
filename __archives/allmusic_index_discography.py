#!/usr/bin/env python
from allmusic_parse_discography import *
from globals import *
import requests

def indexDiscography(artistId): 
    with open(computeDiscographyFileName(artistId), 'r') as f:
        artist = f.read()
        requests.put('http://localhost:4080/api/artist/_doc/' + artistId, 
            data=artist,
            auth=('admin', 'Complexpass#123'))

def main():
    artistId = 'celtic-frost-mn0000191063'
    indexDiscography(artistId)


if __name__ == "__main__":
    main()