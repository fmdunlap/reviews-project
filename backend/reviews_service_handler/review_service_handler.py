"""This module contains the ReviewServiceHandler class, which is responsible for
handling requests to the review service."""

import json
from http.server import SimpleHTTPRequestHandler
from typing import TypedDict, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from regex import compile as re_compile
from lib.db import ReviewsDB

# This is probably overkill for this service, but it's nice to use this TypedDict to
# help keep this a bit more extensible.


class ReviewsParams(TypedDict):
    """The parameters for the reviews endpoint."""
    app_id: str


class ReviewServiceHandler(SimpleHTTPRequestHandler):
    """A handler for the get requests to the service."""

    # That the app_id is only validated as a string of numbers is a bit of a naive
    # assumption, but should work fine here.
    APP_ID_REGEX = re_compile(r"^[0-9]*$")

    def get_db(self) -> ReviewsDB:
        """Get the database.

        Not ideal, but I can only use built in libraries ;)
        """
        if 'db' not in self.__dict__:
            self.db = ReviewsDB()
        return self.db

    def _app_id_is_valid(self, app_id: str) -> bool:
        """Validate the app id is a string of numbers."""
        return self.APP_ID_REGEX.match(app_id) is not None

    def _parse_app_id(self, path: str) -> str | None:
        """Parse the app id from the path."""
        search_params = parse_qs(urlparse(path).query)

        if "app_id" not in search_params:
            self.send_error(
                400,
                "Bad Request",
                "app_id param was not provided. Please provide an app_id in the URL"
            )
            return

        if search_params['app_id'] == [""]:
            self.send_error(
                400,
                "Bad Request",
                "app_id param was not provided. Please provide an app_id in the URL"
            )
            return

        if len(search_params['app_id']) > 1:
            self.send_error(
                400,
                "Bad Request",
                "app_id param was provided multiple times. Provide only one app_id in the URL"
            )
            return

        if not self._app_id_is_valid(search_params['app_id'][0]):
            self.send_error(
                400,
                "Bad Request",
                "app_id param was not valid. Please provide a valid app_id in the URL")
            return

        return search_params['app_id'][0]

    def _parse_params(self, path: str) -> Tuple[ReviewsParams | None, bool]:
        app_id = self._parse_app_id(path)

        if app_id is None:
            return None, False

        return {'app_id': app_id}, True

    def _send_json_response(self, status_code: int, body: dict):
        """Send a JSON response."""
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(json.dumps(body, default=str).encode('utf-8'))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header(
            'Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(ReviewServiceHandler, self).end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        path = self.path

        # ;)
        if path == "/favicon.ico":
            with open('./winking-face-emoji-ico.png', 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(f.read())
            return

        if path.startswith("/reviews"):
            self.handle_reviews_get(path)
            return

        self.send_error(404, "Not Found.")

    def handle_reviews_get(self, path):
        """Handle GET requests to /reviews."""
        params, success = self._parse_params(path)

        if not success:
            # We've already sent the error response.
            return

        app_id = params['app_id']
        if not self.get_db().app_id_exists(app_id):
            self.send_error(404, "Not Found.")
            return

        reviews = self.get_db().get_reviews_since(
            app_id, datetime.now() - timedelta(days=2))
        return self._send_json_response(200, reviews)
