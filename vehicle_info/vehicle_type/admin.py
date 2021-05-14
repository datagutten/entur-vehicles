from django.contrib import admin

# Register your models here.
from .models import ExpectedVehicle, Operator, Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['type', 'length', 'year', 'num_prefix', 'numlow', 'numhigh']


admin.site.register(Vehicle, VehicleAdmin)


admin.site.register(ExpectedVehicle)


class OperatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_prefix']


admin.site.register(Operator, OperatorAdmin)
