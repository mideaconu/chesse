from typing import Any, Callable

import grpc
import grpc_interceptor
from chesse.v1alpha1 import backend_service_pb2
from loguru import logger

from backend.utils import exception


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
            return method(request, context)
        except exception.BackendServerError as e:
            logger.error(str(e))
            context.set_details(str(e))
            context.set_code(e.status_code)
            return getattr(backend_service_pb2, f"{method_name.split('/')[-1]}Response")()
