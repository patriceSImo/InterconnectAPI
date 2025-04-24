from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class InoCxTask(models.Model):
    id_inocx_task = models.AutoField(primary_key=True)
    id_cible = models.CharField(max_length=191)
    id_cxxxxe_sender=models.CharField(max_length=191)
    attempt_number = models.IntegerField(null=True, blank=True)
    contact_id = models.CharField(max_length=255, blank=True)
    id_salesforce = models.CharField(max_length=255)
    datetime_alarm = models.DateTimeField(null=True, blank=True)
    datetime_request = models.DateTimeField(null=True, blank=True)
    displayed_number = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    pin_uxxx_sender = models.CharField(max_length=191)
    status = models.IntegerField(null=True, blank=True)
    payload_json = models.JSONField(null=True, blank=True)  # le corps de l'API (stockée en JSON)
    start_point=models.CharField(max_length=255)
    code_back_call=models.TextField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inoCx_task_followup'

    def __str__(self):
        return f"Task {self.id_salesforce} - {self.contact}"
