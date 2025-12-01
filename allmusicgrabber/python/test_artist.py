#!/usr/bin/env python
from allmusicgrabber.artist import compute_allmusic_artist_url


def main():
    artistId = 'celtic-frost-mn0000191063'
    compute_allmusic_artist_url(artistId)

if __name__ == "__main__":
    main()