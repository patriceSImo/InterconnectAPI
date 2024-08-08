from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from rest_framework.permissions import AllowAny


logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        logger.debug(f"Tentative de connexion avec le nom d'utilisateur : {username}")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            logger.debug("Authentification réussie")
            refresh = RefreshToken.for_user(user)
            response = Response()

            response.data = {
                'message': 'Connexion réussie',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }

            return response
        else:
            logger.debug("Identifiants invalides")
            return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logger.debug("Tentative de déconnexion")
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.debug("Token de rafraîchissement manquant")
                return Response({'message': 'Token de rafraîchissement manquant'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response()
            response.data = {
                'message': 'Déconnexion réussie',
            }
            logger.debug("Déconnexion réussie")
            return response
        except Exception as e:
            logger.error(f"Tentative de déconnexion non autorisée : {str(e)}")
            return Response({'message': 'Non autorisé', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)