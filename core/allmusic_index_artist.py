#!/usr/bin/env python
from allmusicgrabber.globals import *
import requests

def indexArtist(artistId): 
    with open(computeArtistFileName(artistId), 'r') as f:
        artist = f.read()
        requests.put('http://localhost:4080/api/artist/_doc/' + artistId, 
            data=artist,
            auth=('admin', 'Complexpass#123'))

def main():
    artistId = 'celtic-frost-mn0000191063'
    indexArtist(artistId)


if __name__ == "__main__":
    main()