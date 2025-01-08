from rest_framework.views import exception_handler
import os

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 401:
        response.data = {
            'detail': 'Page not found'
        }

    return response


def get_env_variable(var_name):
    """Get the environment variable or raise an exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f"The {var_name} environment variable is not set.")

