from http.server import SimpleHTTPRequestHandler
from regex import compile as re_compile
from typing import TypedDict
from urllib.parse import urlparse, parse_qs

# This is probably overkill for this service, but it's nice to use this TypedDict to
# help keep this a bit more extensible.
class ReviewsParams(TypedDict):
    app_id: str

class ReviewServiceHandler(SimpleHTTPRequestHandler):

    # That the appid is only validated as a string of numbers is a bit of a naive
    # assumption, but should work fine here.
    APP_ID_REGEX = re_compile(r"^[0-9]*$")

    def _app_id_is_valid(self, app_id: str) -> bool:
        """Validate the app id is a string of numbers."""
        return self.APP_ID_REGEX.match(app_id) is not None
    
    def _parse_app_id(self, path: str) -> str | None:
        """Parse the app id from the path."""
        search_params = parse_qs(urlparse(path).query)

        if "id" not in search_params:
            self.send_error(400, "Bad Request.", "AppId was not provided. Please provide an AppId in the URL.")
            return
        
        if search_params['id'] == [""]:
            self.send_error(400, "Bad Request.", "AppId was not provided. Please provide an AppId in the URL.")
            return
        
        if len(search_params['id']) > 1:
            self.send_error(400, "Bad Request.", "AppId was provided multiple times. Please provide only one AppId in the URL.")
            return
        
        if not self._app_id_is_valid(search_params['id'][0]):
            self.send_error(400, "Bad Request.", "AppId was not valid. Please provide a valid AppId in the URL.")
            return

        return search_params['id'][0]
    
    def _parse_params(self, path: str) -> (ReviewsParams | None, bool):
        app_id = self._parse_app_id(path)

        if app_id is None:
            return None, False
        
        return {'app_id': app_id}, True

    def do_GET(self):
        """Handle GET requests."""
        path = self.path

        # This is a little hacky; but it's technically accurate for this service
        if not path.startswith("/reviews"):
            self.send_error(404, "Not Found.")
            return

        self.handle_reviews_GET(path)

    
    def handle_reviews_GET(self, path):
        """Handle GET requests to /reviews."""
        params, success = self._parse_params(path)

        if not success:
            return

        app_id = params['app_id']
        
        # Now that we've got the app_id, look it up in the db, and return the most
        # recent 48 hours of reviews.