from django.db import models, connections
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid
import json
import logging

logger = logging.getLogger(__name__)

class APICall(models.Model):
    id_api_call = models.AutoField(primary_key=True)
    contact_id = models.CharField(max_length=255, blank=True)
    id_salesforce = models.CharField(max_length=255)
    datetime_alarm = models.CharField(max_length=255)
    datetime_request = models.CharField(max_length=255)
    displayed_number = models.CharField(max_length=20)
    pin = models.CharField(max_length=21, null=True, blank=True)
    company = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location = models.TextField(blank =True)
    site = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    payload_json = models.JSONField(null=True, blank=True) 
    response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'apicall'

    def __str__(self):
        return f'{self.method} {self.endpoint}'

    def clean(self):
        """Appelée avant la sauvegarde pour valider et corriger les champs JSON."""
        self.headers = self.validate_json_field(self.headers)
        self.response = self.validate_json_field(self.response)

    def validate_json_field(self, data):
        if not data:
            return {}
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                if isinstance(json_data, dict):
                    return json_data
            except json.JSONDecodeError:
                return {}  # Si la chaîne JSON est mal formée, retourner un dictionnaire vide
        elif isinstance(data, dict):
            return data
        return {}  # Si ce n'est ni une chaîne JSON valide ni un dictionnaire, retourner un dictionnaire vide


class APICallWifirst(models.Model):
    id_todo_from_wifirst = models.AutoField(primary_key=True)
    id_api_call = models.CharField(max_length=191)  # Limitez la longueur à 191 caractères
    contact_id = models.CharField(max_length=255, null=True, blank=True)
    id_salesforce = models.CharField(max_length=255)
    datetime_alarm = models.CharField(max_length=255)
    datetime_request = models.CharField(max_length=255)
    displayed_number = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location = models.TextField(blank =True)
    site = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    pin_ulex_sender = models.TextField(blank=True)
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    payload_json = models.JSONField(null=True, blank=True)  # le corps de l'API (stockée en JSON)
    api_response= models.TextField(null=True, blank=True)
    created_at = models.CharField(max_length=255)

    class Meta:
        db_table = 'todo_from_wifirst'
    
    def clean(self):
        """Appelée avant la sauvegarde pour valider et corriger les champs JSON."""
        self.headers = self.validate_json_field(self.headers)
        self.response = self.validate_json_field(self.response)

    def validate_json_field(self, field):
        """Vérifie que le champ JSON est valide, sinon retourne un dictionnaire vide."""
        try:
            if isinstance(field, str):
                return json.loads(field)
            return field
        except ValueError:
            return {}


class TransmittedAPICall(models.Model):
    id_transmitted = models.AutoField(primary_key=True)
    api_call = models.ForeignKey('APICall', on_delete=models.CASCADE)
    transmitted_to = models.CharField(max_length=191)
    transmitted_status = models.IntegerField()
    transmitted_response = models.JSONField(null=True, blank=True)
    transmitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transmitted_apicall'

class APICallStatistics(models.Model):
    id_api_call_stat = models.AutoField(primary_key=True)
    endpoint = models.CharField(max_length=191, blank=True)
    method = models.CharField(max_length=10, blank=True)
    headers = models.JSONField(null=True, blank=True)
    ip_hote = models.CharField(blank=True, max_length=50)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_call_statistics'

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status}"
    
class APIRequestLog(models.Model):
    request_data = models.JSONField()
    response_data = models.JSONField()
    response_status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request Log - Status: {self.response_status} at {self.created_at}"

    class Meta:
        db_table = 'wifirst_request_log'
