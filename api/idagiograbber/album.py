import requests
import json
import os
from jsonpath_ng.ext import parse



HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def save_json_to_file(data, output_dir, filename, *, ensure_ascii=False, indent=2):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
    return file_path

def extract_with_jsonpath(data, jsonpath_expr, *, first=True, default=None):
    """
    Extract data using a JSONPath expression.

    - first=True  -> returns first match (or default if none)
    - first=False -> returns list of all matches (possibly empty)
    """
    expr = parse(jsonpath_expr)
    matches = [m.value for m in expr.find(data)]

    if not matches:
        return default

    return matches[0] if first else matches

def extract_album_subdata(data):
    extract_data = {}
    extract_data |= { "id": extract_with_jsonpath(data,"$.result.id") }
    extract_data |= { "title": extract_with_jsonpath(data,"$.result.title") }
    extract_data |= { "participants": extract_with_jsonpath(data,"$.result.participants[*].name") }
    return extract_data

def download_html_album_data_from_api(album_url_id, output_dir, verify=True):
    url = f"https://api.idagio.com/v2.0/albums/{album_url_id}"

    resp = requests.get(url, headers=HEADERS, verify=verify, timeout=15)
    resp.raise_for_status()

    data = resp.json()

    extracted = extract_album_subdata(data)
    save_json_to_file(extracted, output_dir, f"{album_url_id}-extract.json")
    save_json_to_file(data, output_dir, f"{album_url_id}.json")
    return data