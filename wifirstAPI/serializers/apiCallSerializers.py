import re
from rest_framework import serializers
from ..models.apiCallModel import APICall

class APICallSerializer(serializers.ModelSerializer):
    class Meta:
        model = APICall
        fields = '__all__'

    def validate_phone(self, value):
        phone_pattern = re.compile(r'^\+33\d{9}$')
        if not phone_pattern.match(value):
            raise serializers.ValidationError('Invalid phone number format. It should be in the format +33XXXXXXXXX')
        return value

    def validate(self, data):
        required_fields = ['id_salesforce', 'company', 'contact', 'phone']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            raise serializers.ValidationError(f'Missing fields: {", ".join(missing_fields)}')
        
        return data
