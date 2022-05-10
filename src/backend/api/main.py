import os
from concurrent import futures

import grpc
import pyfiglet
from chesse_backend_api.v1alpha1 import chesse_pb2 as chesse_pb2_v1alpha1
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import add_CheSSEBackendServiceServicer_to_server
from dotenv import load_dotenv
from grpc_reflection.v1alpha import reflection
from loguru import logger

load_dotenv()

from backend.api import __version__
from backend.api.v1alpha1.server import CheSSEBackendService as CheSSEBackendServiceV1Alpha1


def serve(port: str, max_workers: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_CheSSEBackendServiceServicer_to_server(CheSSEBackendServiceV1Alpha1(), server)

    service_names = (
        chesse_pb2_v1alpha1.DESCRIPTOR.services_by_name["CheSSEBackendService"].full_name,
        reflection.SERVICE_NAME,
    )

    logger.info(f"Creating services: {service_names}...")
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port(f"[::]:{port}")

    server.start()
    startup_banner = pyfiglet.Figlet(font="slant", width=100).renderText("CheSSE Backend API")
    logger.info(f"\n{startup_banner}")
    logger.info(f"Version: {__version__}")
    logger.info(f"Host: localhost:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.getenv("BACKEND_API_PORT")
    max_workers = int(os.getenv("BACKEND_API_MAX_WORKERS"))

    serve(port, max_workers)
