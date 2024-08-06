"""
Global error logging of the entire application
"""
import logging
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exc, context)

    # Add the logging of the exception
    if response is not None:
        logger.error(f"Exception: {exc} - Context: {context}")

    return response