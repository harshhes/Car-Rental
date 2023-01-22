from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from .mixins import *

class Profile(Timestampedmodel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.user.first_name

class VehicleStation(Timestampedmodel):
    station_name = models.CharField(max_length=20)

    def __str__(self):
        return self.station_name


class Vehicle(Timestampedmodel):
    station = models.ForeignKey(VehicleStation,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    company = models.CharField(max_length=20)
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class VehicleHistory(Timestampedmodel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    vehicle_station = models.ForeignKey(VehicleStation, on_delete=models.DO_NOTHING,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    picked_at = models.DateTimeField(default=timezone.now)
    droped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('vehicle', 'user') 