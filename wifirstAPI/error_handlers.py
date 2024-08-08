from django.shortcuts import render

def custom_404_view(request, exception=None):
    response = render(request, '404.html')
    response.status_code = 404
    return response

def custom_401_view(request, exception=None):
    response = render(request, '401.html')
    response.status_code = 401
    return response
