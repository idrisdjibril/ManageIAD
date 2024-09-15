# data_import/serializers.py

from rest_framework import serializers
from .models import DHSI2

class DHSI2Serializer(serializers.ModelSerializer):
    class Meta:
        model = DHSI2
        fields = '__all__'