from allmusicgrabber.globals import fetch_allmusic_html_content


def main():
    # Example: Fetch AllMusic artist page
    url = "https://www.allmusic.com/artist/dismember-mn0000171969"
    print(f"Fetching content from: {url}")
    
    content = fetch_allmusic_html_content(url)
    with open("../data/allmusic/artists/raw/dismember-mn0000171969.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    if content:
        print(f"Successfully fetched {len(content)} characters")
        print("Content preview:")
        print(content[:500])
    else:
        print("Failed to fetch content")

if __name__ == "__main__":
    main()
