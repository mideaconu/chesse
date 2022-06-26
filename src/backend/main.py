import os
from concurrent import futures

import grpc
import structlog
from chesse.v1alpha1 import services_pb2, services_pb2_grpc
from dotenv import load_dotenv
from grpc_reflection.v1alpha import reflection

load_dotenv()

from backend import __version__, tracing
from backend.server.v1alpha1 import interceptor
from backend.server.v1alpha1 import service as v1a1_service

structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="@timestamp"),
        structlog.processors.JSONRenderer(sort_keys=True),
    ]
)
logger = structlog.get_logger()

backend_server_port = int(os.getenv("SERVER_PORT", "50051"))
structlog.contextvars.bind_contextvars(service_port=str(backend_server_port))


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
        logger.info("started server")
        backend_server.wait_for_termination()
    except KeyboardInterrupt:
        backend_server.stop(grace=None)
        logger.info("stopped server")
        structlog.contextvars.clear_contextvars()


if __name__ == "__main__":
    serve(backend_server_port)
