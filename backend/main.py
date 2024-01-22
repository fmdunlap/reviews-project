from http.server import HTTPServer;
from review_service_handler import ReviewServiceHandler;
import multiprocessing

HTTP_PORT = 8000

def start_http_server():
    print(f"🚀 Starting server on port {HTTP_PORT}")
    server = HTTPServer(("localhost", HTTP_PORT), ReviewServiceHandler)
    server.serve_forever()

def start_rss_polling_server():
    print(f"📡 Starting RSS polling server")
    pass

if __name__ == "__main__":
    printf(f"🔥🔥 Starting Review Service 🔥🔥")
    multiprocessing.Process(target=start_http_server).start()
    multiprocessing.Process(target=start_rss_polling_server).start()