import os

from dotenv import load_dotenv

load_dotenv()

from backend import server, tracing

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_SERVER_PORT", "50051"))
    max_workers = int(os.getenv("BACKEND_SERVER_MAX_WORKERS", "10"))

    chesse_backend_server = server.BackendServer(port=port, max_workers=max_workers)
    try:
        chesse_backend_server.run()
    except KeyboardInterrupt:
        chesse_backend_server.stop()