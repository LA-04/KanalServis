from rest_framework import serializers
from .models import kanalservis

class kanalservis_serializer(serializers.ModelSerializer):
    class Meta:
        model = kanalservis
        fields = '__all__'