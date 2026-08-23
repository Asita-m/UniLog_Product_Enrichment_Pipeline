import requests

from src.models.source import Source


def fetch_source(source: Source) -> dict:
    """
    Download a source and return raw response data.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0 Safari/537.36"
        )
    }

    response = requests.get(
        source.url,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return {
        "url": response.url,
        "status_code": response.status_code,
        "content_type": response.headers.get(
            "Content-Type"
        ),
        "html": response.text,
    }
