import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import RawPostDataException
import json
from wifirstAPI.models.apiCallModel import APICall, APICallStatistics
from wifirstAPI.models.apiTokensModels import APIToken
from datetime import datetime
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import pytz

logger = logging.getLogger('wifirstAPI')

class APICallLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Ignorer les requêtes vers l'admin et les fichiers de traduction
        if request.path.startswith('/admin/') or request.path.startswith('/jsi18n/'):
            return response

        # Utiliser une propriété de la requête pour s'assurer que le middleware ne s'exécute qu'une fois
        if hasattr(request, '_api_call_logged'):
            return response
        request._api_call_logged = True

        error_message = None
        response_data = None
        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError:
            response_data = response.content.decode()
        
        if response.status_code != 200:
            error_message = response_data if isinstance(response_data, str) else response_data.get('detail')

        # Enregistrement de toutes les requêtes dans la base de données existante
            api_call = APICall.objects.create(
                contact_id=request.POST.get('contact_id'),
                id_salesforce=request.POST.get('id_salesforce', ''),
                datetime_alarm=request.POST.get('datetime_alarm', ''),
                datetime_request=request.POST.get('datetime_request', ''),
                company=request.POST.get('company', ''),
                contact=request.POST.get('contact', ''),
                location=request.POST.get('location', ''),
                displayed_number=request.POST.get('displayed_number', ''),
                phone=request.POST.get('phone', ''),
                endpoint=request.path,
                method=request.method,
                headers=dict(request.headers),
                status=response.status_code,
                response=response_data,
                error_message=error_message
            )

        # Enregistrement des statistiques dans la nouvelle table
        APICallStatistics.objects.create(
            endpoint=request.path,
            method=request.method,
            headers=dict(request.headers),
            status=response.status_code
        )

        logger.debug(f"API call logged: {api_call}")

        return response

    def get_request_body(self, request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            try:
                if hasattr(request, '_body'):
                    body = json.loads(request.body)
                else:
                    request._body = request.body
                    body = json.loads(request._body)
                logger.debug(f"Request body: {body}")
                return body
            except (json.JSONDecodeError, RawPostDataException) as e:
                logger.error(f"Error decoding request body: {e}")
                return {}
        return {}

    def get_response_body(self, response):
        try:
            response_body = json.loads(response.content)
            logger.debug(f"Response body: {response_body}")
            return response_body
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding response body: {e}")
            return response.content.decode()

class APITokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.debug("APITokenMiddleware appelé")
        
        # Liste des chemins à ignorer
        paths_to_ignore = [
            '/wifirst/login/',
            '/admin/login/',
            '/wifirst/refresh/',
            '/admin/',
            '/static/',
            '/favicon.ico'
    ]
        if any(request.path.startswith(path) for path in paths_to_ignore):
            return self.get_response(request)
        
        api_token = request.headers.get('X-API-Token')
        jwt_token = request.headers.get('Authorization')

        if api_token:
            try:
                # Remove Bearer prefix if exists
                if api_token.startswith("Bearer "):
                    api_token = api_token[7:]
                token = APIToken.objects.get(token=api_token, expires_at__gte=datetime.now(pytz.utc))
                request.user = token.user
                logger.debug(f"API token valide. Utilisateur défini sur : {request.user}")
            except APIToken.DoesNotExist:
                logger.warning(f"API token invalide ou expiré : {api_token}")
                return JsonResponse({'erreur': 'API token invalide ou expiré'}, status=401)
            except Exception as e:
                logger.error(f"Erreur lors de la vérification du token: {e}")
                return JsonResponse({'erreur': 'Erreur interne lors de la vérification du token'}, status=500)
        elif jwt_token:
            jwt_authenticator = JWTAuthentication()
            try:
                validated_token = jwt_authenticator.get_validated_token(jwt_token.split(' ')[1])
                request.user = jwt_authenticator.get_user(validated_token)
                logger.debug(f"JWT token valide. Utilisateur défini sur : {request.user}")
            except (InvalidToken, TokenError) as e:
                logger.warning(f"JWT token invalide ou expiré : {jwt_token}")
                return JsonResponse({'erreur': 'JWT token invalide ou expiré'}, status=401)
            except Exception as e:
                logger.error(f"Erreur lors de la vérification du JWT token: {e}")
                return JsonResponse({'erreur': 'Erreur interne lors de la vérification du JWT token'}, status=500)
        else:
            return JsonResponse({'erreur': 'Aucun token fourni'}, status=401)

        return self.get_response(request)