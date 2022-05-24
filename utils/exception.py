from typing import Callable

import loguru

import grpc


def set_error_context(
    context: grpc.ServicerContext,
    details: str,
    status_code: grpc.StatusCode,
) -> None:
    context.set_details(details)
    context.set_code(status_code)


def log_and_raise(logger: loguru._logger.Logger, error: Callable, error_message: str) -> None:
    logger.error(error_message)
    raise error(error_message)


class SimilarityEncodingError(Exception):
    ...


class CheSSEBackendServerError(Exception):
    ...


class FailedPreconditionError(CheSSEBackendServerError):
    status_code = grpc.StatusCode.FAILED_PRECONDITION


class InvalidFENError(FailedPreconditionError):
    ...


class NotFoundError(CheSSEBackendServerError):
    status_code = grpc.StatusCode.NOT_FOUND


class InternalServerError(CheSSEBackendServerError):
    status_code = grpc.StatusCode.INTERNAL


class InvalidCredentialsError(InternalServerError):
    ...


class IllegalArgumentError(InternalServerError):
    ...


class ElasticSearchQueryError(InternalServerError):
    ...
