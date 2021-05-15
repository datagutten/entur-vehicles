from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from vehicle_type import info
from vehicle_type.models import Vehicle
from .models import VehicleLog


def vehicle_log(request, vehicle_id):
    try:
        prefix, number = info.split_number(vehicle_id)
        vehicle = info.vehicle_type(number, prefix=prefix)
        title = '%s vogn %d' % (vehicle.operator, number)
    except ObjectDoesNotExist:
        vehicle = None
        number = vehicle_id
        title = 'Vogn %d' % number

    logs = VehicleLog.objects.filter(vehicle_ref=vehicle_id)

    logs = logs.filter(
        origin_departure_time__year=datetime.now().year).select_related(
        'line', 'origin', 'origin__Stop')
    lines_seen = {}
    if not logs:
        last_seen = VehicleLog.objects.filter(vehicle_ref=vehicle_id).first()
    else:
        last_seen = None
        for log in logs:
            if not log.line_id or log.line_id in lines_seen:
                continue
            lines_seen[log.line_id] = log.line

    return render(request, 'vehicle_log/vehicle_log.html', {
        'vehicle': vehicle,
        'logs': logs,
        'lines_seen': lines_seen,
        'vehicle_id': vehicle_id,
        'number': number,
        'last_seen': last_seen,
        'title': title
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

    return render(request, 'vehicle_log/line_log.htm', {
        'title': 'Vogner sett på linje %s' % line,
        'line_id': line,
        'vehicles': vehicles_obj.items()
    })


def block_ref_log(request, block_ref):
    logs = VehicleLog.objects.filter(block_ref=block_ref)
    return render(request, 'vehicle_log/logs_table.html', {'logs': logs})


def index(request):
    return render(request, 'vehicle_log/index.html')
