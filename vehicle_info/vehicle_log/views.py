from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from rutedata.models import Line
from vehicle_type import info
from vehicle_type.models import Vehicle
from .models import VehicleLog


def vehicle_log(request, vehicle_id):
    try:
        prefix, number = info.split_number(vehicle_id)
        vehicle = info.vehicle_type(number, prefix=prefix)
        title = '%s vogn %d' % (vehicle.operator.name_string(), number)
    except ObjectDoesNotExist:
        vehicle = None
        number = vehicle_id
        title = 'Vogn %s' % number

    logs = VehicleLog.objects.filter(vehicle_ref=vehicle_id)

    logs = logs.filter(
        origin_departure_time__year=datetime.now().year).select_related(
        'line', 'origin', 'origin__Stop')
    lines_seen = {}
    if not logs:
        last_seen = VehicleLog.objects.filter(vehicle_ref=vehicle_id).first()
    else:
        last_seen = None
        lines_seen = logs.exclude(line=None).values('line').distinct().order_by('line')
        lines_seen = Line.objects.filter(id__in=lines_seen)

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
    line_obj = Line.objects.get(id=line)
    logs = VehicleLog.objects.filter(line__id=line)

    vehicles = logs.values('vehicle_ref').distinct().order_by('vehicle_ref')
    logs = logs.select_related(
        'line', 'origin', 'origin__Stop', 'operator')
    logs = logs.filter(origin_departure_time__year=datetime.now().year)[:30]

    vehicles_obj = {}
    for vehicle in vehicles:
        key = vehicle['vehicle_ref']
        try:
            vehicle = info.vehicle_type(prefixed_number=vehicle['vehicle_ref'])
            vehicles_obj[key] = vehicle
        except Vehicle.DoesNotExist:
            vehicles_obj[key] = vehicle['vehicle_ref']

    return render(request, 'vehicle_log/line_log.htm', {
        'title': 'Linje %s' % line_obj,
        'line_obj': line_obj,
        'vehicles': vehicles_obj.items(),
        'logs': logs,
    })


def block_ref_log(request, block_ref):
    logs = VehicleLog.objects.filter(
        block_ref=block_ref,
        origin_departure_time__year=datetime.now().year).select_related(
        'line', 'origin', 'origin__Stop', 'destination')
    return render(request, 'vehicle_log/block_ref_log.html',
                  {'logs': logs, 'title': 'Vognløp %s' % block_ref})


def index(request):
    return render(request, 'vehicle_log/index.html')
