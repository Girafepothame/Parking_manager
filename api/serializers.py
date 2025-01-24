from rest_framework import serializers
from .models import Parking, Spot

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id', 'name', 'location']

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ['id', 'parking', 'spot_number', 'status']