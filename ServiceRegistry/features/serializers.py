from rest_framework import serializers

from .models import Service


class ServiceAddSerializer(serializers.ModelSerializer):
    """
    It's use for add and edit service records, it has called on ServiceViewSet.
    """
    class Meta:
        model = Service
        fields = ('service', 'version', 'change')


class ServiceRetriveSerializer(serializers.ModelSerializer):
    """
    This serializer used on to retrive services records from service model.
    """
    class Meta:
        model = Service
        fields = ('id', 'service', 'version', 'change')
