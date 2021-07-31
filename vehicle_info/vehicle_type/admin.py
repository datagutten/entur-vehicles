from django.contrib import admin

# Register your models here.
from .models import ExpectedVehicle, Operator, Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['type', 'length', 'year', 'vehicle_prefix', 'numlow', 'numhigh']
    list_filter = ['operator', 'fuel']
    save_as = True


admin.site.register(Vehicle, VehicleAdmin)


admin.site.register(ExpectedVehicle)


class OperatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle_prefix']


admin.site.register(Operator, OperatorAdmin)
