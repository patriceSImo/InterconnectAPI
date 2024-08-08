from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from ..models.apiTokensModels import APIToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger('wifirstAPI')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_api_token(request):
    logger.debug("Entrée dans la vue generate_api_token")
    user = request.user
    logger.debug(f"Utilisateur authentifié: {user.username}")
    
    try:
        logger.debug("Début du bloc try")
        
        token, created = APIToken.objects.get_or_create(user=user)
        logger.debug(f"Token obtenu ou créé: {token}, Créé: {created}")
        
        # Mettre à jour l'expiration du token existant
        if not created:
            token.expires_at = datetime.now() + timedelta(days=3650)  # 10 ans
            token.save()
            logger.debug(f"Expiration du token mise à jour: {token.expires_at}")
        
        return JsonResponse({'token': str(token.token), 'expires_at': token.expires_at}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erreur lors de la génération du token: {e}")
        return JsonResponse({'error': 'Erreur lors de la génération du token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RevokeAPITokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.debug("Tentative de révocation du token")
        try:
            api_token = request.data.get("api_token")
            logger.debug(f"voici le token recupéré {api_token}")
            if not api_token:
                logger.debug("Token manquant")
                return Response({'message': 'Token manquant dans le body de la requette'}, status=status.HTTP_400_BAD_REQUEST)

            token = APIToken.objects.get(token=api_token)
            token.delete()

            response = Response()
            response.data = {
                'message': 'Token révoqué avec succès',
            }
            logger.debug("Révocation réussie")
            return response
        except APIToken.DoesNotExist:
            logger.error("Pas de token à long terme trouvé")
            return Response({'error': 'No API token found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur lors de la révocation du token: {str(e)}")
            return Response({'error': 'Erreur interne lors de la révocation du token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)