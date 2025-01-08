import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import RawPostDataException, JsonResponse
import json
from ..models.apiCallModel import APICall, APICallStatistics
from ..models.apiTokensModels import APIToken
from datetime import datetime
import pytz
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import RawPostDataException

logger = logging.getLogger('wifirstAPI')

class APICallLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        logger.debug(f"Processing response for request path: {request.path}")
        
        if request.path.startswith('/admin/') or request.path.startswith('/jsi18n/'):
            return response
        
        if hasattr(request, '_api_call_logged'):
            logger.debug("Request already logged, skipping.")
            return response
        
        request._api_call_logged = True
        error_message = None
        response_data = None

        try:
            # Extraire le corps de la réponse
            response_data = json.loads(response.content)
            logger.debug(f"Response content: {response_data}")
        except json.JSONDecodeError:
            response_data = response.content.decode()
            logger.debug(f"Response content (decoded): {response_data}")
        
        if response.status_code not in [200, 201]:
            error_message = response_data if isinstance(response_data, str) else response_data.get('detail')
            logger.warning(f"Error message detected: {error_message}")
        
        try:
            # Vérifier si request._body existe et contient des données
            if not hasattr(request, '_body') or request._body is None:
                logger.error("Le corps de la requête n'est pas disponible dans request._body")
                return response
            
            # Créer l'entrée APICallStatistics et stocker dans full_request
            stat_call = APICallStatistics.objects.create(
                endpoint=request.get_full_path(),
                method=request.method,
                headers=dict(request.headers),
                ip_hote=request.META.get('HTTP_HOST'),
                status=response.status_code
            )
            logger.debug(f"API call statistics logged successfully: {stat_call}")
        except Exception as e:
            logger.error(f"Error creating API call statistics entry: {e}")

        return response


    def get_request_body(self, request):
        if hasattr(request, 'data'):
            return request.data
        try:
            return json.loads(request.body)
        except (json.JSONDecodeError, RawPostDataException) as e:
            logger.error(f"Error decoding request body: {e}")
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
        logger.debug("APITokenMiddleware called")
        
        paths_to_ignore = [
            '/comete/login/',
            '/admin/login/',
            '/refresh/',
            '/admin/',
            '/static/',
            '/favicon.ico',
            '/jsi18n/'
        ]
        
        if any(request.path.startswith(path) for path in paths_to_ignore):
            logger.debug(f"Path {request.path} is in the ignore list, skipping token validation.")
            return self.get_response(request)
        
        api_token = request.headers.get('X-API-Token')
        jwt_token = request.headers.get('Authorization')
        logger.debug(f"Received API token: {api_token}")
        logger.debug(f"Received JWT token: {jwt_token}")
        
        if api_token:
            if not self.process_api_token(api_token, request):
                return JsonResponse({'erreur': 'API token invalide ou expiré'}, status=401)
        elif jwt_token:
            if not self.process_jwt_token(jwt_token, request):
                return JsonResponse({'erreur': 'JWT token invalide ou expiré'}, status=401)
        else:
            logger.warning("No token provided")
            return JsonResponse({'erreur': 'Aucun token fourni'}, status=401)

        return self.get_response(request)

    def process_api_token(self, api_token, request):
        try:
            if api_token.startswith("Bearer "):
                api_token = api_token[7:]
            logger.debug(f"Processing API token: {api_token}")
            token = APIToken.objects.get(token=api_token, expires_at__gte=datetime.now(pytz.utc))
            request.user = token.user
            logger.debug(f"API token is valid. User set to: {request.user}")
            return True
        except APIToken.DoesNotExist:
            logger.warning(f"API token invalid or expired: {api_token}")
            return False
        except Exception as e:
            logger.error(f"Error verifying API token: {e}")
            return False

    def process_jwt_token(self, jwt_token, request):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(jwt_token.split(' ')[1])
            request.user = jwt_authenticator.get_user(validated_token)
            logger.debug(f"JWT token is valid. User set to: {request.user}")
            return True
        except (InvalidToken, TokenError) as e:
            logger.warning(f"JWT token invalid or expired: {jwt_token}")
            return False
        except Exception as e:
            logger.error(f"Error verifying JWT token: {e}")
            return False
