#!/usr/bin/env python
import os
from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

load_dotenv()

rootDataDirectory = '../data'
allmusicArtistBaseUrl = 'https://www.allmusic.com/artist/'
rawHTMLFileNameSuffix = '.xml'

# Lecture de la variable d'environnement pour verify
# Valeurs acceptées : "true", "1", "false", "0" (insensibles à la casse)
verify_env = os.getenv("VERIFY_SSL", "false").lower()
VERIFY_SSL = verify_env in ["true", "1", "yes", "y"]
PLAYWRIGHT_TIMEOUT_MS = int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "30000"))
ALLMUSIC_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Artist main page
def computeArtistRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/artist/HTML/' + artistId + rawHTMLFileNameSuffix

def computeArtistFileName(artistId):
    return os.path.abspath(rootDataDirectory + '/allmusic/artist/' + artistId + '.json')

# Discography
def computeDiscographyRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/HTML/' + artistId + rawHTMLFileNameSuffix

def computeDiscographyFileName(artistId):
    return rootDataDirectory + '/allmusic/discography/' + artistId

# Related
def computeRelatedRawHTMLFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId + rawHTMLFileNameSuffix

def computeRelatedFileName(artistId):
    return rootDataDirectory + '/allmusic/related/' + artistId


def fetch_allmusic_html_content(url,referer=None):
    """Load an AllMusic document in Chromium and return its rendered HTML."""
    navigation_referer = referer or "https://www.allmusic.com/"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=ALLMUSIC_USER_AGENT,
                locale="en-US",
                ignore_https_errors=not VERIFY_SSL,
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.5",
                },
            )
            page = context.new_page()
            page.set_default_timeout(PLAYWRIGHT_TIMEOUT_MS)
            response = page.goto(
                url,
                referer=navigation_referer,
                wait_until="domcontentloaded",
                timeout=PLAYWRIGHT_TIMEOUT_MS,
            )
            if response is None:
                raise PlaywrightError("No response was received while navigating")
            if not response.ok:
                raise PlaywrightError(
                    f"AllMusic returned HTTP {response.status} for {url}"
                )
            html_content = page.content()
            context.close()
            browser.close()
            return html_content
    except PlaywrightTimeoutError:
        print(f"AllMusic navigation timed out after {PLAYWRIGHT_TIMEOUT_MS} ms: {url}")
        return None
    except PlaywrightError as error:
        print(f"Une erreur s'est produite dans fetch Playwright : {error}")
        return None
