from typing import Any, Callable, Dict

import grpc
import loguru


def set_error_context(
    context: grpc.ServicerContext,
    details: str,
    status_code: grpc.StatusCode,
) -> None:
    context.set_details(details)
    context.set_code(status_code)


def log_and_raise(
    logger: loguru._logger.Logger, error_cls: Callable, error_args: Dict[str, Any]
) -> None:
    error = error_cls(**error_args)
    logger.error(str(error))
    raise error


class SimilarityEncodingError(Exception):
    ...


class BackendServerError(Exception):
    ...


class InvalidFENEncodingError(BackendServerError):
    status_code = grpc.StatusCode.INVALID_ARGUMENT

    def __init__(self, fen_encoding: str, message: str) -> None:
        self.fen_encoding = fen_encoding
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error processing FEN encoding {self.fen_encoding!r}: {self.message}"


class InvalidCredentialsError(BackendServerError):
    status_code = grpc.StatusCode.FAILED_PRECONDITION

    def __init__(self, service: str, message: str) -> None:
        self.service = service
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error authenticating to {self.service}: {self.message}"


class SearchEngineQueryError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL

    def __init__(self, query: Dict[str, Any], message: str) -> None:
        self.query = query
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error running query {self.query}: {self.message}"


class SearchEnginePbConversionError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL

    def __init__(self, response: Dict[str, Any], message: str) -> None:
        self.response = response
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error converting query response {self.response} to pb object: {self.message}"


class NotFoundError(BackendServerError):
    status_code = grpc.StatusCode.NOT_FOUND


class InternalServerError(BackendServerError):
    status_code = grpc.StatusCode.INTERNAL


class IllegalArgumentError(InternalServerError):
    ...


class ElasticSearchQueryError(InternalServerError):
    ...
