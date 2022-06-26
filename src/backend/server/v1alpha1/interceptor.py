from typing import Any, Callable

import grpc
import grpc_interceptor
import structlog
from chesse.v1alpha1 import backend_service_pb2

from backend.tracing import trace
from backend.utils import exception

logger = structlog.get_logger()


class ExceptionToStatusInterceptor(grpc_interceptor.ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        """Override this method to implement a custom interceptor.

        You should call method(request, context) to invoke the
        next handler (either the RPC method implementation, or the
        next interceptor in the list).

        Args:
            method: The next interceptor, or method implementation.
            request: The RPC request, as a protobuf message.
            context: The ServicerContext pass by gRPC to the service.
            method_name: A string of the form
            "/protobuf.package.Service/Method"

        Returns:
            This should generally return the result of
            method(request, context), which is typically the RPC
            method response, as a protobuf message. The interceptor
            is free to modify this in some way, however.
        """
        try:
            structlog.threadlocal.clear_threadlocal()
            span_context = trace.get_current_span().get_span_context()
            structlog.threadlocal.bind_threadlocal(
                request_method=method.__name__,
                trace_id=span_context.trace_id,
                span_id=span_context.span_id,
            )
            response = method(request, context)
            logger.info("request successful")
            structlog.threadlocal.clear_threadlocal()
            return response
        except exception.BackendServerError as e:
            logger.error(
                "backend server error",
                error_type=type(e).__name__,
                error_message=str(e),
                status_code=e.status_code.value[1],
            )
            context.set_details(str(e))
            context.set_code(e.status_code)
            return getattr(backend_service_pb2, f"{method_name.split('/')[-1]}Response")()
        except Exception as e:
            logger.error(
                "backend server error",
                error_type=type(e).__name__,
                error_message=str(e),
                status_code=grpc.StatusCode.UNKNOWN.value[1],
            )
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return getattr(backend_service_pb2, f"{method_name.split('/')[-1]}Response")()
