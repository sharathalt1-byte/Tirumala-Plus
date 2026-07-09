import requests
import urllib3

from tirumala_pulse.config.settings import TTD_NEWS_BASE_URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TTDNewsAPI:

    def __init__(self):
        self.base_url = TTD_NEWS_BASE_URL

    def get_posts(self, page=1, per_page=5):

        response = requests.get(
            f"{self.base_url}/wp-json/wp/v2/posts",
            params={
                "page": page,
                "per_page": per_page,
                "_fields": "id,date,title,link,content,categories"
            },
            headers={
                "User-Agent": "Tirumala Pulse ETL/1.0"
            },
            timeout=30,
            verify=False      # Development only
        )

        response.raise_for_status()

        return response.json()