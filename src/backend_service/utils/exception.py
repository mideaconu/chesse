import grpc


def set_error_context(
    context: grpc.ServicerContext,
    details: str,
    status_code: grpc.StatusCode,
) -> None:
    context.set_details(details)
    context.set_code(status_code)


class BackendServerError(Exception):
    ...


class InvalidFENEncodingError(BackendServerError):
    status_code = grpc.StatusCode.INVALID_ARGUMENT


class InvalidCredentialsError(BackendServerError):
    status_code = grpc.StatusCode.FAILED_PRECONDITION


class SearchEngineQueryError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL


class SearchEnginePbConversionError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL


class NotFoundError(BackendServerError):
    status_code = grpc.StatusCode.NOT_FOUND


class InternalServerError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL


class IllegalArgumentError(InternalServerError):
    ...
