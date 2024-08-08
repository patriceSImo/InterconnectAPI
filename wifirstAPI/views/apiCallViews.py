import requests
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models.apiCallModel import APICall
from ..serializers.apiCallSerializers import APICallSerializer
import json
import logging

logger = logging.getLogger('wifirstAPI')

class APICallViewSet(viewsets.ModelViewSet):
    queryset = APICall.objects.all()
    serializer_class = APICallSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Vérification des en-têtes requis
        required_headers = ['X-Method', 'X-Headers']
        missing_headers = [header for header in required_headers if header not in request.headers]
        if missing_headers:
            return Response(
                {"error": f"Missing required headers: {', '.join(missing_headers)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extraction des en-têtes
        endpoint = request.headers.get('X-Endpoint')
        method = request.headers.get('X-Method')
        headers = request.headers.get('X-Headers')
        
        logger.debug(f"Endpoint: {endpoint}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Headers: {headers}")

        try:
            headers = json.loads(headers)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format in X-Headers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Envoyer la requête à l'endpoint spécifié
        try:
            response = requests.request(method, endpoint, headers=headers, json=request.data)
            response_status = response.status_code
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            response_status = 200
            response_data = {'error_message': str(e)}

        # Sauvegarder l'appel API dans la base de données
        api_call = APICall.objects.create(
            contact_id=serializer.validated_data['contact_id'],
            id_salesforce=serializer.validated_data['id_salesforce'],
            datetime_alarm=serializer.validated_data['datetime_alarm'],
            datetime_request=serializer.validated_data['datetime_request'],
            company=serializer.validated_data['company'],
            contact=serializer.validated_data['contact'],
            location=serializer.validated_data['location'],
            displayed_number=serializer.validated_data['displayed_number'],
            phone=serializer.validated_data['phone'],
            endpoint=endpoint,
            method=method,
            headers=headers,
            status=response_status,
            response=response_data if response_status == 200 else None,
            error_message=response_data.get('error_message') if response_status != 200 else None
        )

        if response_status == 200:
            salesforce_body = {
                "OwnerId": "005AY000008C5BQYA0",
                "Comments": "appel au client en cours",
                "RecordTypeId": "0125I000000cLpiQAE",
                "Status": "En-cours"
            }
        else:
            salesforce_body = {
                "OwnerId": "005AY000008C5BQYA0",
                "Comments": f"NATURE DE L'ERREUR: {response_data.get('error_message', 'Erreur inconnue')}"
            }

        # Retourner la réponse à l'utilisateur
        return Response(
            {
                'id': api_call.id,
                'message': 'Success: Your request has been processed successfully' if response_status == 200 else 'Error: There was an issue processing your request',
                'status': response_status,
                'displayed_number': serializer.validated_data['phone'],
                'salesfore_body': salesforce_body
            },
            status=status.HTTP_201_CREATED if response_status == 200 else status.HTTP_400_BAD_REQUEST
        )