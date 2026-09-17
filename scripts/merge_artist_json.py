import argparse
import copy
import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        document = json.load(file)

    if not isinstance(document, dict) or not isinstance(document.get("data"), dict):
        raise ValueError(f"{path} must contain a JSON object with a 'data' object")
    return document


def normalize_title(title: str) -> str:
    return " ".join(title.split()).casefold()


def merge_discography(
    allmusic_discography: list[Any], discogs_releases: list[Any]
) -> list[Any]:
    releases_by_title: dict[str, list[dict[str, Any]]] = {}
    for release in discogs_releases:
        if not isinstance(release, dict) or not isinstance(release.get("title"), str):
            continue
        title = normalize_title(release["title"])
        releases_by_title.setdefault(title, []).append(release)

    merged_discography = copy.deepcopy(allmusic_discography)
    for album in merged_discography:
        if not isinstance(album, dict) or not isinstance(album.get("albumTitle"), str):
            continue
        title = normalize_title(album["albumTitle"])
        album["discogs"] = copy.deepcopy(releases_by_title.get(title, []))

    return merged_discography


def write_allmusic_discography_csv(
    path: Path,
    allmusic_document: dict[str, Any],
    overwrite: bool,
) -> None:
    data = allmusic_document["data"]
    fieldnames = [
        "artistId",
        "artistName",
        "albumYear",
        "albumTitle",
        "musicRating",
        "avgRating",
    ]
    mode = "w" if overwrite else "x"
    with path.open(mode, encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for album in data["discography"]:
            writer.writerow(
                {
                    "artistId": allmusic_document.get("artistId", ""),
                    "artistName": data["name"],
                    "albumYear": album.get("albumYear", ""),
                    "albumTitle": album.get("albumTitle", ""),
                    "musicRating": album.get("musicRating", ""),
                    "avgRating": album.get("avgRating", ""),
                }
            )


def write_discogs_discography_csv(
    path: Path,
    discogs_document: dict[str, Any],
    overwrite: bool,
) -> None:
    releases = discogs_document["data"]["discography"]["releases"]
    fieldnames = [
        "id",
        "title",
        "artist",
        "year",
        "type",
        "role",
        "mainRelease",
        "status",
        "format",
        "label",
        "resourceUrl",
        "thumbnailUrl",
        "inWantlist",
        "inCollection",
    ]
    mode = "w" if overwrite else "x"
    with path.open(mode, encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for release in releases:
            community = release.get("stats", {}).get("community", {})
            writer.writerow(
                {
                    "id": release.get("id", ""),
                    "title": release.get("title", ""),
                    "artist": release.get("artist", ""),
                    "year": release.get("year", ""),
                    "type": release.get("type", ""),
                    "role": release.get("role", ""),
                    "mainRelease": release.get("main_release", ""),
                    "status": release.get("status", ""),
                    "format": release.get("format", ""),
                    "label": release.get("label", ""),
                    "resourceUrl": release.get("resource_url", ""),
                    "thumbnailUrl": release.get("thumb", ""),
                    "inWantlist": community.get("in_wantlist", ""),
                    "inCollection": community.get("in_collection", ""),
                }
            )


def merge_artist(
    allmusic_document: dict[str, Any], discogs_document: dict[str, Any]
) -> dict[str, Any]:
    allmusic_data = allmusic_document.get("data")
    discogs_data = discogs_document.get("data")
    if not isinstance(allmusic_data, dict) or not isinstance(discogs_data, dict):
        raise ValueError("Both documents must contain a 'data' object")

    allmusic_name = allmusic_data.get("name")
    discogs_name = discogs_data.get("name")
    if not isinstance(allmusic_name, str) or not isinstance(discogs_name, str):
        raise ValueError("Both documents must contain a string 'data.name'")
    if allmusic_name.casefold() != discogs_name.casefold():
        raise ValueError(
            f"Artist names do not match: {allmusic_name!r} and {discogs_name!r}"
        )

    # discography
    
    allmusic_discography = allmusic_data.get("discography")
    
    discogs_discography = discogs_data.get("discography")
    if not isinstance(allmusic_discography, list):
        raise ValueError("The AllMusic document must contain a 'data.discography' list")
    if not isinstance(discogs_discography, dict) or not isinstance(
        discogs_discography.get("releases"), list
    ):
        raise ValueError(
            "The Discogs document must contain a 'data.discography.releases' list"
        )

    merged = copy.deepcopy(allmusic_document)
    merged["data"]["discography"] = merge_discography(
        allmusic_discography, discogs_discography["releases"]
    )
    merged["data"]["discogs"] = copy.deepcopy(discogs_document)
    return merged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add Discogs artist data to an authoritative AllMusic JSON file."
    )
    parser.add_argument("allmusic_file", type=Path)
    parser.add_argument("discogs_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument(
        "--csv-output",
        type=Path,
        help="CSV path (defaults to <output>-allmusic-discography.csv)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace the output file if it already exists",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    allmusic_document = load_json(args.allmusic_file)
    discogs_document = load_json(args.discogs_file)
    merged = merge_artist(
        allmusic_document,
        discogs_document,
    )

    allmusic_csv_output = args.csv_output or args.output_file.with_name(
        f"{args.output_file.stem}-allmusic-discography.csv"
    )
    discogs_csv_output = args.output_file.with_name(
        f"{args.output_file.stem}-discogs-discography.csv"
    )
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    allmusic_csv_output.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.overwrite else "x"
    with args.output_file.open(mode, encoding="utf-8", newline="\n") as file:
        json.dump(merged, file, ensure_ascii=False, indent=2)
        file.write("\n")
    write_allmusic_discography_csv(
        allmusic_csv_output, allmusic_document, args.overwrite
    )
    write_discogs_discography_csv(
        discogs_csv_output, discogs_document, args.overwrite
    )

    print(f"Merged artist written to {args.output_file}")
    print(f"AllMusic discography written to {allmusic_csv_output}")
    print(f"Discogs discography written to {discogs_csv_output}")


if __name__ == "__main__":
    main()