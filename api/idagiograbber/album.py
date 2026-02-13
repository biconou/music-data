import requests
from bs4 import BeautifulSoup
import json
import os
import re

HEADERS = {
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


def scrape_idagio_album(url: str, output_dir: str | None = None, save_html: bool = False):
    """
    Fonction principale de scraping :
    - télécharge la page
    - extrait les albums depuis les scripts ld+json
    - éventuellement sauvegarde les JSON et le HTML
    - renvoie { "albums": [...] }
    """
    resp = requests.get(url, headers=HEADERS, verify=False, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"Erreur HTTP {resp.status_code} pour URL {url}")

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # 1) Extraire le JSON des balises <script type="application/ld+json">
    ld_json_blocks = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # On ignore les scripts invalides
            continue
        ld_json_blocks.append(data)

    # 2) Construire albums[]
    albums = extract_albums_from_ld_json(ld_json_blocks)
    output = {"albums": albums}

    # 3) Sauvegarde sur disque (optionnelle)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # Sauvegarder chaque album en JSON
        for album in albums:
            album_name = album.get("name", "album")
            artists = album.get("byArtist", [])

            if artists:
                artists_str = "_".join(artists)
                base_name = f"{album_name}__{artists_str}"
            else:
                base_name = album_name

            safe_name = slugify(base_name)
            file_path = os.path.join(output_dir, f"{safe_name}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(album, f, ensure_ascii=False, indent=2)

        # Sauvegarder le HTML brut (si demandé)
        if save_html:
            html_path = os.path.join(output_dir, "idagio_album.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

    return output


    """
    Endpoint POST /extract-album
    Body JSON attendu :
    {
      "url": "https://app.idagio.com/fr/albums/archora-aion",
      "save_to_disk": true,           # optionnel
      "output_dir": "C:/chemin/...",  # optionnel
      "save_html": false              # optionnel
    }
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "Champ 'url' requis dans le JSON d'entrée"}), 400

    save_to_disk = data.get("save_to_disk", False)
    save_html = data.get("save_html", False)
    output_dir = data.get("output_dir") if save_to_disk else None

    if save_to_disk and not output_dir:
        # Si l'utilisateur veut sauvegarder mais ne précise pas de dossier,
        # on utilise DEFAULT_OUTPUT_DIR
        output_dir = DEFAULT_OUTPUT_DIR

    try:
        result = scrape_idagio_album(url, output_dir=output_dir, save_html=save_html)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

