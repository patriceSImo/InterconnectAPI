from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views
from xxxxxxxAPI.custom_404_view import custom_404_view
from wxxxxxtAPI.custom_401_view import custom_401_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='admin-login'),
    path('admin/', admin.site.urls),
    path('cxxxxe/', include('wxxxxxtAPI.urls.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = custom_404_view
handler401 = custom_401_view
