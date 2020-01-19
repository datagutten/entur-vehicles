from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from vehicle_type.info import VehicleInfo
from vehicle_type.models import Vehicle
from .models import VehicleLog


def vehicle_log(request, vehicle_id):
    try:
        vehicle = VehicleInfo.info(vehicle_id)
    except ObjectDoesNotExist:
        vehicle = None

    try:
        lines = VehicleInfo.seen_on(vehicle_id)
    except ObjectDoesNotExist:
        lines = None

    logs = VehicleLog.objects.filter(vehicle_ref=vehicle_id)
    logs = logs.order_by('origin_departure_time').reverse()

    prefix, number = VehicleInfo.parse_number(vehicle_id)

    return render(request, 'vehicle_log/vehicle_log.html', {
                           'vehicle': vehicle,
                           'logs': logs,
                           'lines': lines,
                           'vehicle_id': vehicle_id,
                           'prefix': prefix,
                           'number': number
    })


def line_log(request, line):
    from vehicle_type.info import VehicleInfo
    logs = VehicleLog.objects.filter(line_ref=line)

    vehicles = logs.values('vehicle_ref').distinct().order_by('vehicle_ref')

    vehicles_obj = {}
    for vehicle in vehicles:
        key = vehicle['vehicle_ref']
        try:
            vehicle = VehicleInfo.info(vehicle['vehicle_ref'])
            vehicles_obj[key] = vehicle
        except Vehicle.DoesNotExist:
            vehicles_obj[key] = vehicle['vehicle_ref']

    return render(request, 'vehicle_log/line_log.htm', {'vehicles': vehicles_obj.items()})
