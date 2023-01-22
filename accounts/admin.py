from django.contrib import admin
from .models import *


# @admin.register(Profile)
# class AdminProfile(admin.ModelAdmin):
#     # user = 
#     # list_display = ['user'

admin.site.register(Profile)
admin.site.register(Vehicle)
admin.site.register(VehicleStation)
admin.site.register(VehicleHistory)