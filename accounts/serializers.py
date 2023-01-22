from rest_framework import serializers
from .models import *


class AddVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        fields = "__all__"
        model = Vehicle

    def create(self, validated_data):
        vehicle_id = validated_data['vehicle_id']
        vehicle_history = VehicleHistory.objects.create(vehicle=vehicle_id)
        
        return validated_data

class VehicleStationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = VehicleStation

class VehicleHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = "__all__"
        model = VehicleHistory

    # drop a vehicle post-usage
    def update(self, instance, validated_data):
        # print(instance, validated_data)
        vehicle_station = validated_data['vehicle_station']
        droped_at = validated_data['droped_at']
        vehicle = instance.vehicle.id
        station_update = Vehicle.objects.get(id=vehicle)
        droped_at_update = VehicleHistory.objects.get(vehicle=vehicle)
        droped_at_update.droped_at = droped_at
        station_update.station = vehicle_station
        station_update.save()
        droped_at_update.save()
        print(station_update.name, station_update.station.station_name)
        
        return instance