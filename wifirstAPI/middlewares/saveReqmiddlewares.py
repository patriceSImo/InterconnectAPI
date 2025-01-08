from ..models.apiCallModel import APIRequestLog
from django.http import HttpResponseServerError

class ReqStatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture les informations de la requête
        request_data = {
            "method": request.method,
            "path": request.path,
            "headers": dict(request.headers),
            "body": request.body.decode('utf-8') if request.body else None,
        }

        # Appelle la vue ou le middleware suivant
        response = self.get_response(request)

        # Capture les informations de la réponse
        response_data = {
            "status_code": response.status_code,
            "body": response.content.decode('utf-8') if response.content else None
        }

        # Enregistrement de la requête et de la réponse en base de données
        APIRequestLog.objects.create(
            request_data=request_data,
            response_data=response_data,
            response_status=response.status_code
        )

        return response


class ErrorHandlingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        if response.status_code == 500:
            response = HttpResponseServerError("System cannot be accessed", content_type="text/plain", status=500)
    
        return response