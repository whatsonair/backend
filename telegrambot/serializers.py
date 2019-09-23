from .models import RadioStation
from rest_framework import serializers


class RadioStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadioStation
        fields = ['href', 'name', 'url', 'monitor', 'scrapper']