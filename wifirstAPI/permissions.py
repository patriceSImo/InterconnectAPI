from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
import logging

logger = logging.getLogger(__name__)

class IsAuthenticatedOrNotFound(BasePermission):
    """
    Custom permission to return 404 Not Found for unauthenticated users.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            logger.info("User is authenticated")
            return True
        logger.info("User is not authenticated")
        raise NotFound(detail="Page not found")
