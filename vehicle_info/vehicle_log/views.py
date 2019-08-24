from django.shortcuts import render
from .models import VehicleLog


def show_log(request, vehicle):
    logs = VehicleLog.objects.filter(vehicle_ref=vehicle)
    vehicle_obj = logs.first().vehicle_type
    logs = logs.order_by('origin_departure_time')
    return render(request, 'vehicle_log/logs.html', {'logs': logs, 'vehicle': vehicle_obj})
