import os

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from structlog import contextvars

load_dotenv()

from backend import __version__ as service_version

service_name = os.getenv("SERVICE_NAME")
service_type = os.getenv("SERVICE_TYPE")

contextvars.bind_contextvars(
    service_name=service_name, service_version=service_version, service_type=service_type
)

resource = Resource(attributes={"service.name": service_name, "service.version": service_version})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

grpc_server_instrumentor = GrpcInstrumentorServer().instrument()
