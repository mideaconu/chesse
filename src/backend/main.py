import os
from concurrent import futures

import grpc
import pyfiglet
from chesse.v1alpha1 import services_pb2, services_pb2_grpc
from dotenv import load_dotenv
from grpc_reflection.v1alpha import reflection
from loguru import logger

from backend import __version__

load_dotenv()

from backend import tracing
from backend.server.v1alpha1 import interceptor
from backend.server.v1alpha1 import service as v1a1_service


def _print_startup_banner() -> None:
    """Generates a startup banner in the server logs."""
    figlet = pyfiglet.Figlet(font="slant", width=150)
    banner = figlet.renderText(f"CheSSE Backend Server v{__version__}")
    logger.info(f"\n\n{banner}")


def serve(port: int) -> None:
    backend_server = grpc.server(
        futures.ThreadPoolExecutor(),
        interceptors=[interceptor.ExceptionToStatusInterceptor()],
    )
    services_pb2_grpc.add_BackendServiceServicer_to_server(
        v1a1_service.BackendService(), backend_server
    )

    service_names = (
        services_pb2.DESCRIPTOR.services_by_name["BackendService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, backend_server)

    try:
        backend_server.add_insecure_port(f"[::]:{port}")
        backend_server.start()
        _print_startup_banner()
        backend_server.wait_for_termination()
    except KeyboardInterrupt:
        backend_server.stop(grace=None)


if __name__ == "__main__":
    port = int(os.getenv("BACKEND_SERVER_PORT", "50051"))
    serve(port)
