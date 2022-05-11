import os

from dotenv import load_dotenv

load_dotenv()

from backend.api import server

if __name__ == "__main__":
    server = server.CheSSEBackendServer(
        port=int(os.getenv("BACKEND_API_PORT")),
        max_workers=int(os.getenv("BACKEND_API_MAX_WORKERS")),
    )
    server.run()
