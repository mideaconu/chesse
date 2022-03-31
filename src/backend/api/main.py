from concurrent import futures

import grpc
from chesse_backend_api.v1alpha1 import chesse_pb2 as chesse_pb2_v1alpha1
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import add_CheSSEBackendServiceServicer_to_server
from dotenv import load_dotenv
from grpc_reflection.v1alpha import reflection

load_dotenv()

from backend.api import __version__
from backend.api.v1alpha1.server import CheSSEBackendService as CheSSEBackendServiceV1Alpha1
from utils import logger

LOGGER = logger.get_logger(__name__)


def serve(port: str, max_workers: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_CheSSEBackendServiceServicer_to_server(CheSSEBackendServiceV1Alpha1(), server)

    SERVICE_NAMES = (
        chesse_pb2_v1alpha1.DESCRIPTOR.services_by_name["CheSSEBackendService"].full_name,
        reflection.SERVICE_NAME,
    )

    LOGGER.info("Creating services: %s", SERVICE_NAMES)
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:%s" % port)

    server.start()
    LOGGER.info("%s: %s started", server, __version__)
    server.wait_for_termination()


if __name__ == "__main__":
    port = "50051"
    max_workers = 10

    LOGGER.info("Starting CheSSE Backend Service version %s", __version__)
    LOGGER.info("Starting CheSSE Backend Service on port: %s", port)
    LOGGER.info("Starting CheSSE Backend Service with max_workers: %s", max_workers)

    serve(port, max_workers)
