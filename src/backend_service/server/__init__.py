from concurrent import futures

import grpc
import pyfiglet
from chesse.v1alpha1 import services_pb2, services_pb2_grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

from backend_service import __version__
from backend_service.server.v1alpha1 import service as v1alpha1_service
from backend_service.utils import meta


class BackendServer(metaclass=meta.Singleton):
    def __init__(self, port: int = 50051, max_workers: int = 10) -> None:
        logger.info("Initialising CheSSE Backend Server...")
        self.version = __version__
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

        services_pb2_grpc.add_BackendServiceServicer_to_server(
            v1alpha1_service.BackendService(), self.server
        )

        service_names = (
            services_pb2.DESCRIPTOR.services_by_name["BackendService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(service_names, self.server)

    def _print_startup_banner(self) -> None:
        """Generates a startup banner in the server logs."""
        figlet = pyfiglet.Figlet(font="slant", width=150)
        startup_banner = figlet.renderText(f"CheSSE Backend Server v{self.version}")
        logger.info(f"\n\n{startup_banner}")

    def start(self) -> None:
        """Starts the server."""
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()

        self._print_startup_banner()
        logger.info(f"Initialised CheSSE Backend Server on port {self.port}.")

    def run(self) -> None:
        """Starts the server and waits for its termination."""
        self.start()
        self.server.wait_for_termination()

    def stop(self) -> None:
        """Stops the server."""
        self.server.stop(grace=None)
