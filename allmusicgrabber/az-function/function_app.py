import azure.functions as func
import logging
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def json_response(payload, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(payload, sort_keys=False, indent=4),
        status_code=status_code,
        mimetype="application/json"
    )

@app.route(route="find-artist")
def find_artist(req: func.HttpRequest) -> func.HttpResponse:
    query = None
    try:
        # Check if the request has a JSON body
        if req.get_json():
            req_body = req.get_json()
            query = req_body.get('query')
    except ValueError:
        pass  # JSON decoding failed
    # Fallback to query parameters if no JSON body or `query` is missing
    if query is None:
        query = req.params.get('query')
    if query is None:
        return func.HttpResponse(
            json.dumps({'error': 'Query parameter is missing'}),
            status_code=400,
            mimetype="application/json"
        )
    try:
        # Appel de l’API externe
        external_api_url = "https://biconou.freeboxos.fr:501/find-artist"
        params = {"query": query}

        logging.info(f"Calling external API: {external_api_url} with params={params}")
        response = requests.get(external_api_url, params=params, timeout=10)

        # Gestion des erreurs HTTP de l’API externe
        if not response.ok:
            logging.error(
                f"External API returned status {response.status_code}: {response.text}"
            )
            return json_response(
                {
                    "error": "External API error",
                    "status": response.status_code,
                    "details": response.text[:500],
                },
                502,
            )

        # On suppose que l’API renvoie du JSON
        data = response.json()

        # Si besoin, tu peux transformer ici le JSON pour
        # l’adapter à ton format de sortie
        # ex: artist = transform_external_response(data)
        artist = data

        return json_response(artist, 200)
    except requests.RequestException as e:
        logging.error(f"HTTP error when calling external API: {e}")
        return json_response(
            {'error': 'Error while contacting external API'},
            502
        )
    except Exception as e:
        logging.exception("Unexpected error in search-artist")
        return json_response({'error': 'Internal server error'}, 500)


@app.route(route="artist/{artist_id}")
def artist(req: func.HttpRequest) -> func.HttpResponse:
    artist_id = req.route_params.get("artist_id")
    artist_url = compute_allmusic_artist_url(artist_id)
    html_content = fetch_allmusic_html_content(artist_url)
    artist = parse_artist(artist_id,html_content)
    jsonArtist = json.dumps(artist, sort_keys=False, indent=4)
    return json_response(jsonArtist, 500)

