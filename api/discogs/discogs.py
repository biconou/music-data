import os
import requests
from urllib.parse import urlencode
from env_utils import load_api_env


DISCOGS_API_BASE = "https://api.discogs.com"

VERIFY_SSL, DISCOGS_KEY, DISCOGS_SECRET = load_api_env()

def search(query, search_type=None, per_page=10, page=1, **filters):
    """
    Recherche dans Discogs Database API.
    - query: texte libre (ex: "Daft Punk Discovery")
    - search_type: "artist", "release", "master", "label" (optionnel)
    - filters: ex: year=2001, country="France", format="Vinyl"
    """
    url = f"{DISCOGS_API_BASE}/database/search"

    params = {
        "key": DISCOGS_KEY, 
        "secret": DISCOGS_SECRET,
        "q": query,
        "per_page": per_page,
        "page": page,
        **filters,
    }
    if search_type:
        params["type"] = search_type

    headers = {
        "User-Agent": "MyDiscogsSearchApp/1.0 +https://example.com"
    }

    r = requests.get(url, params=params, headers=headers, timeout=30, verify=VERIFY_SSL)
    r.raise_for_status()
    return r.json()

def print_results(data, max_items=10):
    results = data.get("results", [])[:max_items]
    if not results:
        print("Aucun résultat.")
        return

    for i, item in enumerate(results, 1):
        title = item.get("title")
        year = item.get("year")
        country = item.get("country")
        item_type = item.get("type")
        uri = item.get("uri")  # URL relative Discogs
        resource_url = item.get("resource_url")  # URL API de la ressource

        print(f"{i}. [{item_type}] {title} ({year or 'n/a'}, {country or 'n/a'})")
        print(f"   Discogs: https://www.discogs.com{uri}" if uri else "   Discogs: n/a")
        print(f"   API: {resource_url or 'n/a'}")

def main():

    # Exemple 1: recherche libre
    data = search("Daft Punk Discovery", per_page=10)
    print("Recherche libre:")
    print_results(data)

    # Exemple 2: filtrer par type + année
    data = search("Discovery", search_type="release", year=2001, per_page=10)
    print("\nReleases 'Discovery' en 2001:")
    print_results(data)

    # Exemple 3: recherche label
    data = search("Warp", search_type="label", per_page=5)
    print("\nLabels 'Warp':")
    print_results(data, max_items=5)

if __name__ == "__main__":
    main()