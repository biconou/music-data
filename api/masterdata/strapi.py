import requests
from bs4 import BeautifulSoup
import json
import os
import re


def check_artist_id(artist_id):
    url = f"http://locahost:1337/api/artists?filters%5Ballmusic_id%5D={artist_id}"
    
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")
    try:
        data = resp.json()
    except json.JSONDecodeError:
        data = json.loads(resp.text)

    return data



def main():
    # URL d'un album Idagio (remplace par celle que tu veux tester)
    artistId = "dismember"

    try:
        data = check_artist_id(artistId)

        print("Vérification réussie !")
        print("Données reçues :", data)

    except Exception as e:
        print("Erreur lors de la vérification de l'artiste :", e)


if __name__ == "__main__":
    main()