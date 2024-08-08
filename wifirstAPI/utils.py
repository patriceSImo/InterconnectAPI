from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 401:
        response.data = {
            'detail': 'Page not found'
        }

    return response
