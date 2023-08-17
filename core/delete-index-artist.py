#!/usr/bin/env python
import requests

artistId = 'celtic-frost-mn0000191063'

def main():

    requests.delete('http://localhost:4080/api/artist/_doc/' + artistId, 
        auth=('admin', 'Complexpass#123'))


if __name__ == "__main__":
    main()