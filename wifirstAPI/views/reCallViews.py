import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.apiCallModel import APICall

class RetryAPICallView(APIView):
    def post(self, request, pk):
        api_call = get_object_or_404(APICall, pk=pk)
        
        headers = {k: v for k, v in api_call.headers.items()}
        
        try:
            response = requests.request(
                method=api_call.method,
                url=api_call.endpoint,
                headers=headers,
                json=api_call.body
            )
            api_call.status = response.status_code
            api_call.response = response.json()
            api_call.save()

            return Response(api_call.response, status=api_call.status)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
