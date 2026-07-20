import requests
import urllib3

from tirumala_pulse.config.settings import TTD_NEWS_BASE_URL
from tirumala_pulse.config.constants import POSTS_PER_PAGE
from tirumala_pulse.utils.logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger(__name__)


class TTDNewsAPI:
    """
    Client for the official TTD WordPress REST API.
    """

    def __init__(self):
        self.base_url = TTD_NEWS_BASE_URL

    def get_posts(self, page=1):
        """
        Retrieve one page of posts from the TTD News API.
        """

        response = requests.get(
            f"{self.base_url}/wp-json/wp/v2/posts",
            params={
                "page": page,
                "per_page": POSTS_PER_PAGE,
                "_fields": "id,date,title,link,content,categories"
            },
            headers={
                "User-Agent": "Tirumala Pulse ETL/1.0"
            },
            timeout=30,
            verify=False
        )

        response.raise_for_status()

        return response.json()

    def iter_posts(self):
        """
        Stream every post from the TTD News API.

        The API's X-WP-TotalPages header is unreliable,
        so we continue requesting pages until an empty
        page is returned.
        """

        page = 1
        total_posts = 0

        while True:

            logger.info(
                "Downloading page %s",
                page
            )

            posts = self.get_posts(page)

            if not posts:

                logger.info(
                    "No more posts found."
                )

                break

            logger.info(
                "Downloaded %s posts from page %s",
                len(posts),
                page
            )

            for post in posts:

                total_posts += 1

                yield post

            page += 1

        logger.info(
            "Historical download completed."
        )

        logger.info(
            "Total posts streamed: %s",
            total_posts
        )