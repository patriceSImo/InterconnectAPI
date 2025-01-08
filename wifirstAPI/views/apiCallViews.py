import requests
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from ..models.apiCallModel import APICall, APICallWifirst
from ..serializers.apiCallSerializers import APICallSerializer
import json
from io import BytesIO
from django.http import JsonResponse
import logging

logger = logging.getLogger('wifirstAPI')

class APICallViewSet(viewsets.ModelViewSet):
    queryset = APICall.objects.all()
    serializer_class = APICallSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        request._body = request.body

        # Tenter de décoder le corps en JSON
        try:
            request_data = json.loads(request._body.decode('utf-8'))  # Convertir la chaîne JSON en dictionnaire Python
        except json.JSONDecodeError:
            # Si le contenu n'est pas un JSON valide, retourner une erreur
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Assurer que `request_data` est un dictionnaire (JSON valide)
        if not isinstance(request_data, dict):
            return JsonResponse({'error': 'Invalid data format, expected JSON object'}, status=400)

        # Sérialiser les données
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        # Définir un statut et une réponse par défaut
        response_status = 200
        response_data = {
            "message": "Success: Your request has been processed successfully"
        }

        # Sauvegarder l'appel API dans la base de données
        try:
            api_call = APICall.objects.create(
                contact_id=serializer.validated_data.get('contact_id'),
                id_salesforce=serializer.validated_data['id_salesforce'],
                datetime_alarm=serializer.validated_data['datetime_alarm'],
                datetime_request=serializer.validated_data['datetime_request'],
                company=serializer.validated_data['company'],
                contact=serializer.validated_data['contact'],
                pin=serializer.validated_data['caseNumber'],
                location=serializer.validated_data['location'],
                site=serializer.validated_data['site'],
                displayed_number=serializer.validated_data['displayed_number'],
                phone=serializer.validated_data['phone'],
                endpoint=request.path,
                status=response_status,
                payload_json=request_data,
                response=response_data,
            )
            logger.info(f"Appel API sauvegardé avec l'ID {api_call.id_api_call}")
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'appel API: {e}")
            return Response({'error': 'Failed to save API call'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Essayer de dupliquer les données dans APICallWifirst
        try:
            api_call_wifirst = APICallWifirst.objects.create(
                id_api_call=api_call.id_api_call,
                contact_id=api_call.contact_id,
                id_salesforce=api_call.id_salesforce,
                datetime_alarm=api_call.datetime_alarm,
                datetime_request=api_call.datetime_request,
                displayed_number=api_call.displayed_number or "+33170704670",
                company=api_call.company,
                contact=api_call.contact,
                location=api_call.location,
                site=api_call.site,
                phone=api_call.phone,
                endpoint=api_call.endpoint,
                method=request.method,
                headers=dict(request.headers),
                status=api_call.status,
                response=response_data,
                created_at=api_call.created_at,
            )
            logger.info(f"Appel API dupliqué dans Wifirst avec l'ID {api_call_wifirst.id_api_call}")
        except Exception as e:
            logger.error(f"Échec de la duplication de l'appel API dans Wifirst: {e}")
            return Response(
                {"error": f"Échec de la duplication de l'appel API dans Wifirst: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Réinjecter le corps dans le flux pour permettre d'autres lectures (par exemple, dans un middleware)
        request._stream = BytesIO(request._body)
        request._read_started = False

        # Retourner la réponse à l'utilisateur
        return Response(
            {
                'id': api_call.id_api_call,
                'message': 'Success: Your request has been processed successfully' if response_status == 200 else 'Error: There was an issue processing your request',
                'Status': 'En-cours' if response_status == 200 else 'error',
                'RecordTypeId': '0125I000000cLpiQAE',
                'OwnerId': '005Sb0000062kOHIAY',
                'Comments': 'appel au client en cours'
            },
            status=status.HTTP_201_CREATED if response_status == 200 else status.HTTP_400_BAD_REQUEST
        )
