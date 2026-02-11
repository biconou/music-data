import requests
from bs4 import BeautifulSoup
import json
import os
import re

url = "https://app.idagio.com/fr/albums/594cdd9a-728e-4dcb-a751-80a8034d5cc4"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def extract_albums_from_ld_json(ld_json_blocks):
    """
    Prend une liste de blocs JSON (ld_json_blocks) et renvoie
    une liste d'albums normalisés (albums[]).
    """
    albums = []

    for block in ld_json_blocks:
        if isinstance(block, dict) and block.get("@type") and "MusicAlbum" in block["@type"]:
            album_obj = {
                "idagio-id": block.get("@id"),
                "url": block.get("url"),
                "name": block.get("name"),
                "datePublished": block.get("datePublished"),
                "numTracks": block.get("numTracks"),
                "byArtist": [a.get("name") for a in block.get("byArtist", [])],
                "tracks": []
            }

            for track in block.get("track", []):
                recording_of = track.get("recordingOf", {}) or {}
                composer = recording_of.get("composer", {}) or {}

                track_obj = {
                    "name": track.get("name"),
                    "url": track.get("url"),
                    "duration": track.get("duration"),
                    "datePublished": track.get("datePublished"),
                    "byArtist": [a.get("name") for a in track.get("byArtist", [])],
                    "recordingOf": {
                        "name": recording_of.get("name"),
                        "url": recording_of.get("url"),
                        "musicalKey": recording_of.get("musicalKey"),
                        "composer": composer.get("name"),
                        "datePublished": recording_of.get("datePublished"),
                    }
                }
                album_obj["tracks"].append(track_obj)

            albums.append(album_obj)

    return albums


def slugify(value: str) -> str:
    """
    Transforme une chaîne en nom de fichier sûr :
    - minuscules
    - remplace espaces par tirets
    - supprime les caractères non autorisés
    """
    value = value.strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9\-_.]", "", value)
    return value or "album"


response = requests.get(url, headers=headers, verify=False)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Titre de la page
    title = soup.find("title")
    print("Titre de la page :", title.get_text(strip=True) if title else "Non trouvé")

    # 1) Extraire toutes les balises <meta> sous forme de dicts
    metas = []
    for meta in soup.find_all("meta"):
        meta_info = {}
        for attr in ["name", "property", "content", "charset", "http-equiv"]:
            if meta.has_attr(attr):
                meta_info[attr] = meta[attr]
        if meta_info:
            metas.append(meta_info)

    print("=== META TAGS (simples) ===")
    for m in metas:
        print(m)

    # 2) Extraire le JSON des balises <script type="application/ld+json">
    ld_json_blocks = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print("JSON invalide dans un <script type='application/ld+json'>")
            continue
        ld_json_blocks.append(data)

    # 3) Utiliser la fonction factorisée pour construire albums[]
    albums = extract_albums_from_ld_json(ld_json_blocks)

    # 4) Affichage global (optionnel)
    output = {"albums": albums}
    print("\n=== LD+JSON ALBUMS ===")
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # 5) Écrire chaque album dans un fichier "<name>__<artists>.json"
    output_dir = r"C:\DATA\develop\music-data\data\idagio\album"
    os.makedirs(output_dir, exist_ok=True)

    for album in albums:
        album_name = album.get("name", "album")
        artists = album.get("byArtist", [])

        # construire une chaîne avec les artistes, ex: "lorenzo-micheli_matteo-mela"
        if artists:
            artists_str = "_".join(artists)
            base_name = f"{album_name}__{artists_str}"
        else:
            base_name = album_name

        safe_name = slugify(base_name)
        file_path = os.path.join(output_dir, f"{safe_name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(album, f, ensure_ascii=False, indent=2)

        print(f"Album sauvegardé dans '{file_path}'")

    # 6) Sauvegarder le HTML pour debug
    html_path = os.path.join(output_dir, "idagio_album.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML sauvegardé dans '{html_path}'")

else:
    print("Erreur HTTP :", response.status_code)
    print(response.headers)
    print(response.text[:1_000])