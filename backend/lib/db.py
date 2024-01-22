"""A module for interacting with the reviews database."""
import sqlite3
from datetime import datetime
from .review import Review


class ReviewsDB:
    """A class for interacting with the reviews database.

    Note: One of the nice things about using sqlite3 here is that the lib automatically
    escapes all the values, so we don't have to worry about SQL injection attacks.
    """

    def __init__(self):
        self.conn = sqlite3.connect('reviews.db')
        self.cursor = self.conn.cursor()
        self.create_reviews_table()

    def create_reviews_table(self):
        """Create the reviews table if it doesn't exist."""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS reviews (app_id INTEGER, id INTEGER, authorName TEXT, authorUri TEXT, rating TEXT, title TEXT, content TEXT, updated TEXT, version TEXT)")
        self.conn.commit()

    def convert_db_row_to_review(self, db_review: tuple) -> Review:
        """Convert a database row to a Review object."""
        return Review(
            id=db_review[1],
            authorName=db_review[2],
            authorUri=db_review[3],
            rating=db_review[4],
            title=db_review[5],
            content=db_review[6],
            updated=datetime.fromisoformat(db_review[7]),
            version=db_review[8]
        )

    def get_all_reviews(self, app_id: int) -> list[Review]:
        """Get the reviews for an app."""
        self.cursor.execute(
            "SELECT * FROM reviews WHERE app_id = ? ORDER BY updated DESC", (app_id,))
        db_reviews = self.cursor.fetchall()
        return [self.convert_db_row_to_review(db_review) for db_review in db_reviews]

    def get_reviews_since(self, app_id: int, since: datetime) -> list[Review]:
        """Get the reviews for an app since a given time."""
        self.cursor.execute(
            "SELECT * FROM reviews WHERE app_id = ? AND updated > ? ORDER BY updated DESC", (app_id, since.isoformat()))
        db_reviews = self.cursor.fetchall()
        return [self.convert_db_row_to_review(db_review) for db_review in db_reviews]

    def app_id_exists(self, app_id: int) -> bool:
        """Check if an app id exists in the database."""
        self.cursor.execute(
            "SELECT * FROM reviews WHERE app_id = ? LIMIT 1", (app_id,))
        return len(self.cursor.fetchall()) > 0

    def insert_reviews(self, app_id: int, reviews: list[Review]):
        """Insert new reviews into the database."""

        insert_entries = [(
            app_id,
            review['id'],
            review['authorName'],
            review['authorUri'],
            review['rating'],
            review['title'],
            review['content'],
            review['updated'].isoformat(),
            review['version']
        ) for review in reviews]

        self.cursor.executemany(
            "INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (insert_entries))
        self.conn.commit()
