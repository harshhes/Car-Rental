from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name='register'),
    path('login', login_user, name='login_user'),
    path('otp', otp, name='otp'),
    path('login_otp', login_otp, name='login_otp'),
    path('main', main, name='main'),

    path("add_vehicle", AddVehicleView.as_view(), name='add_vehicle'),
    path("vehicle_detail/<int:pk>", DetailVehicleView.as_view(), name='vehicle_detail'), # assign to a station

    path("add_station", VehicleStationView.as_view(), name='add_station'),
    path("vehicle_history/<int:pk>", VehicleHistoryView.as_view(), name='vehicle_history'), # drop a vehicle, enter vehicle_history object id
    path('get_vehicles', GetVehicles.as_view(), name='get_vehicles'),
    path('pick_vehicle', PickVehicle.as_view())
]