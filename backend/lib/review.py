"""A review of an app. This is a subset of the data returned by the RSS feed."""

from typing import TypedDict
from datetime import datetime


class Review(TypedDict):
    """A review of an app."""
    id: int
    authorName: str
    authorUri: str
    rating: int
    title: str
    content: str
    updated: datetime
    version: str
