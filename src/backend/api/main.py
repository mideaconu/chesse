import os

from dotenv import load_dotenv

load_dotenv()

from backend.api import server

if __name__ == "__main__":
    chesse_backend_server = server.CheSSEBackendServer(
        port=int(os.getenv("BACKEND_API_PORT")),
        max_workers=int(os.getenv("BACKEND_API_MAX_WORKERS")),
    )
    chesse_backend_server.run()
