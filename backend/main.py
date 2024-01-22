from http.server import HTTPServer;
from review_service_handler import ReviewServiceHandler;

PORT = 8000

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), ReviewServiceHandler)
    server.serve_forever()