import requests
import urllib3

from tirumala_pulse.config.constants import POSTS_PER_PAGE
from tirumala_pulse.config.settings import TTD_NEWS_BASE_URL
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

        params = {
            "page": page,
            "per_page": POSTS_PER_PAGE,
            "_fields": "id,date,title,link,content,categories",
        }

        response = requests.get(
            self.base_url,
            params=params,
            timeout=30,
            verify=False,
        )

        logger.info("========================================")
        logger.info("Request URL  : %s", response.url)
        logger.info("HTTP Status  : %s", response.status_code)
        logger.info("Content-Type : %s", response.headers.get("Content-Type"))
        logger.info("========================================")

        if response.status_code in (400, 404):
            logger.info("No more pages available.")
            return []

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            logger.error("Response is not valid JSON.")
            logger.error("Response body:\n%s", response.text[:1000])
            return []

        logger.info("Posts returned by API: %s", len(data))

        return data

    def iter_pages(self, start_page=1):
        """
        Stream pages from the TTD News API.
        """

        page = start_page

        while True:

            logger.info("Downloading page %s", page)

            posts = self.get_posts(page)

            logger.info("Posts received on page %s: %s", page, len(posts))

            if not posts:
                logger.info("No more posts found.")
                break

            yield page, posts

            page += 1

    def iter_posts(self, start_page=1):
        """
        Stream individual posts.
        """

        total_posts = 0

        for _, posts in self.iter_pages(start_page):

            for post in posts:
                total_posts += 1
                yield post

        logger.info("Historical download completed.")
        logger.info("Total posts streamed: %s", total_posts)