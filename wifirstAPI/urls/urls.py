from django.urls import path, include
from rest_framework.routers import DefaultRouter
from xxxxxxxAPI.views.apiCallViews import APICallViewSet
from wxxxxxtAPI.views.auth_views import LoginView, LogoutView
from wxxxxxtAPI.views.reCallViews import RetryAPICallView
from wxxxxxtAPI.views.forwardApiCallViews import ForwardAPICallView
from rest_framework_simplejwt.views import TokenRefreshView
from wxxxxxtAPI.views.apiTokenViews import generate_api_token, RevokeAPITokenView

router = DefaultRouter()
router.register(r'calls', APICallViewSet, basename='calls/')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('retry/<int:pk>/', RetryAPICallView.as_view(), name='retry_api_call'),
    path('forward/', ForwardAPICallView.as_view(), name='forward_api_call'),
    path('token/generate/', generate_api_token, name='generate_api_token'),
    path('token/revoke/', RevokeAPITokenView.as_view(), name='revoke_api_token'),
]
