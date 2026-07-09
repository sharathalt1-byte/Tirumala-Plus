import requests

TTD_DARSHAN_URL = "https://news.tirumala.org/category/darshan/"


def fetch_latest_page():
    """
    Downloads the latest TTD Darshan news page.
    """

    response = requests.get(
        TTD_DARSHAN_URL,
        timeout=30,
        headers={
            "User-Agent": "TirumalaPulse/1.0"
        }
    )

    response.raise_for_status()

    return response.text