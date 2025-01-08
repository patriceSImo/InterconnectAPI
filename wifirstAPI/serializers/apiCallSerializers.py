import re
from rest_framework import serializers
from ..models.apiCallModel import APICall
import logging

logger = logging.getLogger(__name__)

class APICallSerializer(serializers.ModelSerializer):
    displayed_number= serializers.CharField(required=False, allow_blank=True, default='')
    location = serializers.CharField(required=False, allow_blank=True, default ='')
    caseNumber = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = APICall
        fields = '__all__'

    def validate_phone_patern(self, value):
        phone_pattern = re.compile(r'^\+33\d{9}$')
        if not phone_pattern.match(value):
            raise serializers.ValidationError('Invalid phone number format. It should be in the format +33XXXXXXXXX')
        return value
    
    def validate_phone(self,value):
        value = re.sub(r'\D','',value)
        value = value [-9:]
        value = '+33' + value
        value = self.validate_phone_patern(value)
        return value
    
    def validate_caseNumber(self, value):
        if value == '':
            return value  # Ne validez pas si le champ est vide

        if not value.isdigit():
            raise serializers.ValidationError("Le PIN doit être un entier.")

        if len(value) >= 9:
            raise serializers.ValidationError("Le PIN doit contenir maximum 6 chiffres.")

        return value


    def validate(self, data):
        required_fields = ['id_salesforce', 'company', 'contact', 'phone']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            raise serializers.ValidationError(f'Missing fields: {", ".join(missing_fields)}')
        
        return data
