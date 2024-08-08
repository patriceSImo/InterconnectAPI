
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.apiCallModel import APICall, TransmittedAPICall

class ForwardAPICallView(APIView):
    def post(self, request):
        # Enregistrer l'appel API reçu
        api_call = APICall.objects.create(
            endpoint=request.path,
            method=request.method,
            headers=dict(request.headers),
            body=request.data,
            status=200,  # Temporaire, sera mis à jour après la transmission
            response={}
        )

        # Définir l'URL de l'API à laquelle transférer la requête
        target_url = "http://example.com/target/api"

        try:
            # Transférer la requête à l'API cible
            response = requests.request(
                method=api_call.method,
                url=target_url,
                headers=api_call.headers,
                json=api_call.body
            )

            # Enregistrer la réponse de l'API cible
            transmitted_call = TransmittedAPICall.objects.create(  
                api_call=api_call,
                transmitted_to=target_url,
                transmitted_status=response.status_code,
                transmitted_response=response.json()
            )

         
            api_call.status = response.status_code
            api_call.response = response.json()
            api_call.save()

            return Response(api_call.response, status=api_call.status)
        except Exception as e:
     
            api_call.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            api_call.response = {"error": str(e)}
            api_call.save()

            return Response(api_call.response, status=api_call.status)