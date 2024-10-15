"""
    contains classes and funtions of general utility
"""

import json

from django.urls import reverse
from django.template.loader import get_template
from rest_framework.response import Response


def make_response(status_code, status_message, status_params=None, data=None):
    """
        Method to build default response object.]
        Params:
            status_code: rest_framework.status Http Code to return
            status_message: i18n id for frontend to present message (e.g., 'error.object-not-found')
            status_params (optional): dictionary with parameters for status message
            data (optional): return data of the endpoint, when applicable
        Returns:
            response: object with standardized response structure
    """
    response = {
        "data": data,
        "status":
        {
            "code": status_code,
            "message": status_message,
            "params": status_params
        }
    }
    return Response(response, status=status_code)
