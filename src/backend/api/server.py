from concurrent import futures

import pyfiglet
from chesse_backend_api.v1alpha1 import chesse_pb2
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import add_CheSSEBackendServiceServicer_to_server
from grpc_reflection.v1alpha import reflection
from loguru import logger

import grpc
from backend.api import __version__
from backend.api.v1alpha1 import service as v1alpha1service


class CheSSEBackendServer:
    def __init__(self, port: int = 50051, max_workers: int = 10):
        logger.info("Initialising CheSSE Backend API server...")
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

        add_CheSSEBackendServiceServicer_to_server(
            v1alpha1service.CheSSEBackendService(), self.server
        )

        service_names = (
            chesse_pb2.DESCRIPTOR.services_by_name["CheSSEBackendService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(service_names, self.server)

    def _print_startup_logs(self) -> None:
        figlet = pyfiglet.Figlet(font="slant", width=150)
        startup_banner = figlet.renderText(f"CheSSE Backend API v{__version__}")
        logger.info(f"\n\n{startup_banner}")
        logger.info(f"Initialised CheSSE Backend API server on port {self.port}.")

    def start(self) -> None:
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()
        self._print_startup_logs()

    def run(self) -> None:
        self.start()
        self.server.wait_for_termination()

    def stop(self) -> None:
        self.server.stop(grace=None)
