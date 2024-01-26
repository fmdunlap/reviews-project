"""Main entry point for the Review Service."""

import multiprocessing
from http.server import HTTPServer
from reviews_service_handler.review_service_handler import ReviewServiceHandler
from rss_polling_service.rss_polling_service import RssPollingService
import config


def _start_http_server():
    print(f"🚀 Starting server on port {config.HTTP_PORT}")
    server = HTTPServer(("localhost", config.HTTP_PORT), ReviewServiceHandler)
    server.serve_forever()


def _start_rss_polling_server():
    print("📡 Starting RSS polling server")
    server = RssPollingService(
        config.SUPPORTED_APP_IDS,
        config.POLLING_INTERVAL,
        config.REVIEW_LOOKBACK_TIMEDELTA
    )
    server.start()


if __name__ == "__main__":
    print("🔥🔥 Starting Review Service 🔥🔥")
    http_server_process = multiprocessing.Process(target=_start_http_server)
    rss_polling_process = multiprocessing.Process(
        target=_start_rss_polling_server)
    try:
        http_server_process.start()
        rss_polling_process.start()
        http_server_process.join()
        rss_polling_process.join()
    except KeyboardInterrupt:
        print("🛑 Stopping Review Service 🛑")
        http_server_process.terminate()
        rss_polling_process.terminate()
