from concurrent import futures

import grpc
from duchess_backend_api.v1alpha1 import duchess_pb2 as duchess_pb2_v1alpha1
from duchess_backend_api.v1alpha1.duchess_pb2_grpc import (
    add_DuchessBackendServiceServicer_to_server,
)
from grpc_reflection.v1alpha import reflection

from backend_api import __version__
from backend_api.v1alpha1.server import (
    DuchessBackendServiceGRPC as DuchessBackendServiceGRPCb1alpha1,
)
from utils import logger

LOGGER = logger.get_logger(__name__)


def serve(port: str, max_workers: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_DuchessBackendServiceServicer_to_server(DuchessBackendServiceGRPCb1alpha1(), server)

    SERVICE_NAMES = (
        duchess_pb2_v1alpha1.DESCRIPTOR.services_by_name["DuchessBackendService"].full_name,
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

    LOGGER.info("Starting Duchess Backend Service version %s", __version__)
    LOGGER.info("Starting Duchess Backend Service on port: %s", port)
    LOGGER.info("Starting Duchess Backend Service with max_workers: %s", max_workers)

    serve(port, max_workers)
