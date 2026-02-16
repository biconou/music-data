from album import download_html_album_page

def main():
    # URL d'un album Idagio (remplace par celle que tu veux tester)
    url = "https://app.idagio.com/fr/albums/the-renaissance-album-DC7BDBB3-4688-4593-8172-4B9204148ABD"

    try:
        html = download_html_album_page(
            url=url,
            verify=True,
            save_html=False  # met à True si tu veux sauvegarder le HTML
        )

        print("Téléchargement réussi !")
        print("Longueur du HTML :", len(html))
        print("\n--- Début du HTML ---\n")
        print(html[:1000])  # affiche les 1000 premiers caractères

    except Exception as e:
        print("Erreur lors du téléchargement :", e)


if __name__ == "__main__":
    main()
