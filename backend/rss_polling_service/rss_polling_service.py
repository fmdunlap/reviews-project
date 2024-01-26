"""A service for polling the RSS feed for reviews for a list of apps."""
import json
import urllib.request
import time
from datetime import datetime, timedelta, timezone
from typing import List
from lib.review import Review
from lib.db import ReviewsDB

APPLE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
APPLE_RSS_URL = "https://itunes.apple.com/us/rss/customerreviews/id={appId}/sortBy=mostRecent/page={page}/json"

DEFAULT_POLLING_INTERVAL = timedelta(minutes=5)
DEFAULT_REVIEW_LOOKBACK_TIMEDELTA = timedelta(days=2)


class RssPollingService():
    """A service for polling the RSS feed for reviews for a list of apps."""

    def __init__(
            self,
            app_id_list: List[int],
            polling_interval: timedelta = DEFAULT_POLLING_INTERVAL,
            review_lookback_timedelta: timedelta = DEFAULT_REVIEW_LOOKBACK_TIMEDELTA
    ):
        """Initialize the RSS polling service. Note, must call start to start polling."""
        self.app_id_list = app_id_list
        self.polling_interval = polling_interval
        self.review_lookback_timedelta = review_lookback_timedelta
        self.db = ReviewsDB()

    def start(self):
        """Start polling the RSS feed for reviews.

        This will poll the RSS feed for reviews for each app in the app_id_list
        """
        while True:
            for app_id in self.app_id_list:
                self.poll_app(app_id)
            time.sleep(self.polling_interval.total_seconds())

    def poll_app(self, app_id: int):
        """Poll the RSS feed for reviews for a given app.

        Args:
            appId: The app id to poll reviews for.
        """
        print(f"Polling app {app_id}...")
        newest_stored_review = self.get_newest_stored_review(app_id)
        remote_reviews = self.get_latest_reviews_from_rss_feed(
            app_id, datetime.now(timezone.utc) - self.review_lookback_timedelta)
        reviews_to_add = []
        for review in remote_reviews:
            if newest_stored_review is None or review['updated'] > newest_stored_review['updated']:
                reviews_to_add.append(review)

        if len(reviews_to_add) > 0:
            self.db.insert_reviews(app_id, reviews_to_add)

        print(f"Added {len(reviews_to_add)} reviews for app {app_id}")

    def get_newest_stored_review(self, app_id: int) -> Review:
        """Get the newest stored review for a given app.

        Args:
            appId: The app id to get the newest stored review for.
        """
        return self.db.get_all_reviews(app_id)[0] if len(self.db.get_all_reviews(app_id)) > 0 else None

    def get_latest_reviews_from_rss_feed(
            self,
            app_id: int,
            oldest_review_time: datetime
    ) -> List[Review]:
        """Get the latest reviews from the RSS feed for a given app.

        Args:
            appId: The app id to get reviews for.
            oldestReviewTime: The oldest review time to get reviews for.
        """
        reviews = []
        page = 1
        while True:
            revews_json = self.fetch_app_reviews(app_id, page)
            reviews_from_page = self.parse_rss_response(revews_json)
            if len(reviews_from_page) == 0:
                break
            for review in reviews_from_page:
                if review['updated'] < oldest_review_time:
                    return reviews
                reviews.append(review)
            page += 1
        return reviews

    def fetch_app_reviews(self, app_id: int, page: int = 1) -> str:
        """Fetch reviews for a given app from the RSS feed.

        Args:
            appId: The app id to fetch reviews for.
            page: The page of reviews to fetch. Defaults to 1.
        """
        req = urllib.request.Request(
            APPLE_RSS_URL.format(appId=app_id, page=page),
            data=None,
            # Spoof the user agent to get the full RSS feed.
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            })

        reviews_json = ''
        with urllib.request.urlopen(req) as response:
            reviews_json = response.read().decode('utf-8')
        return reviews_json

    def parse_rss_response(self, json_string: str) -> List[Review]:
        """Parse the RSS response into a list of reviews.

        Args:
            json_string: The JSON string to parse into reviews.
        """
        reviews = []
        try:
            raw_reviews = json.loads(json_string)['feed']['entry']
            for raw_review in raw_reviews:
                review = Review(
                    id=raw_review['id']['label'],
                    authorName=raw_review['author']['name']['label'],
                    authorUri=raw_review['author']['uri']['label'],
                    rating=int(raw_review['im:rating']['label']),
                    title=raw_review['title']['label'],
                    content=raw_review['content']['label'],
                    updated=datetime.strptime(
                        raw_review['updated']['label'], APPLE_DATETIME_FORMAT).astimezone(timezone.utc),
                    version=raw_review['im:version']['label']
                )
                reviews.append(review)
        except KeyError:
            print(f"Error parsing RSS response {json_string}")
        return reviews


if __name__ == "__main__":
    RssPollingService(app_id_list=[284882215], polling_interval=timedelta(
        minutes=1), review_lookback_timedelta=timedelta(days=2)).start()
