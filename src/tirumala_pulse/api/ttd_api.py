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

        Returns an empty list when:
        - The requested page does not exist (400/404)
        - The response is not valid JSON
        - The API returns an unexpected payload
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

        # WordPress returns 400/404 when the requested page
        # is beyond the available pagination.
        if response.status_code in (400, 404):
            logger.info("No more pages available. Ending backfill.")
            return []

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            logger.warning(
                "Received a non-JSON response for page %s. Ending backfill.",
                page,
            )
            logger.debug("Response body: %s", response.text[:500])
            return []

        if not isinstance(data, list):
            logger.warning(
                "Unexpected API response for page %s. Ending backfill.",
                page,
            )
            return []

        return data

    def iter_pages(self, start_page=1):
        """
        Stream pages from the TTD News API.

        Yields:
            tuple(page_number, posts)
        """

        page = start_page

        while True:

            logger.info("Downloading page %s", page)

            posts = self.get_posts(page)

            if not posts:
                logger.info("No more posts found.")
                break

            logger.info(
                "Downloaded %s posts from page %s",
                len(posts),
                page,
            )

            yield page, posts

            page += 1

    def iter_posts(self, start_page=1):
        """
        Stream individual posts.

        Built on top of iter_pages().
        """

        total_posts = 0

        for _, posts in self.iter_pages(start_page):
            for post in posts:
                total_posts += 1
                yield post

        logger.info("Historical download completed.")
        logger.info("Total posts streamed: %s", total_posts)