import requests
import json
from artist import check_artist_id


def main():
    # URL d'un album Idagio (remplace par celle que tu veux tester)
    artistId = "aerosmith-mn0000604852"

    try:
        data = check_artist_id(artistId)

        print("Vérification réussie !")
        print("Données reçues :", data)

    except Exception as e:
        print("Erreur lors de la vérification de l'artiste :", e)


if __name__ == "__main__":
    main()