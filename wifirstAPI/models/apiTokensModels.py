from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta

def get_default_expiration():
    return datetime.now() + timedelta(days=3650)

class APIToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expiration)

    def __str__(self):
        return str(self.token)
