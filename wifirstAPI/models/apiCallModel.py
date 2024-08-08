from django.db import models

class APICall(models.Model):
    contact_id = models.IntegerField(null= True, blank = True)
    id_salesforce = models.CharField(max_length=255)
    displayed_number = models.CharField(max_length=20)
    datetime_alarm = models.CharField(max_length=255)
    datetime_request = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location = models.TextField()
    phone = models.CharField(max_length=20)
    endpoint = models.CharField(max_length=255,null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f'{self.method} {self.endpoint}'


class TransmittedAPICall(models.Model):
    api_call = models.ForeignKey(APICall, on_delete=models.CASCADE)
    transmitted_to = models.CharField(max_length=255)
    transmitted_status = models.IntegerField()
    transmitted_response = models.JSONField(null=True, blank=True)
    transmitted_at = models.DateTimeField(auto_now_add=True)
  


class APICallStatistics(models.Model):
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=10,null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status}"
    
