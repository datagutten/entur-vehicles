from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from rutedata.models import Line
from vehicle_type import info
from vehicle_type.models import Operator, Vehicle
from .models import VehicleLog

year = datetime.now().year


def vehicle_log(request, vehicle_id=None):
    vehicle_id_get = request.GET.get('vehicle')
    if not vehicle_id and not vehicle_id_get:
        operators = Operator.objects.all()
        return render(request, 'vehicle_log/select_vehicle.html',
                      {'operators': operators})
    elif vehicle_id_get:
        vehicle_id = vehicle_id_get

    prefix, number = info.split_number(vehicle_id)
    try:
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
        'title': title,
        'prefix': prefix,
    })


def line_log(request, line):
    line_obj = Line.objects.get(id=line)
    logs = VehicleLog.objects.filter(line__id=line,
                                     origin_departure_time__year=year).\
        select_related('vehicle_type', 'vehicle_type__operator')

    vehicles_log = logs.order_by('vehicle_ref')
    logs = logs.filter(origin_departure_time__year=datetime.now().year)[:30]

    vehicles_obj = {}
    for log in vehicles_log:
        key = log.vehicle_ref
        if key in vehicles_obj:
            continue
        try:
            vehicles_obj[key] = log.vehicle_type
        except Vehicle.DoesNotExist:
            vehicles_obj[key] = log.vehicle_ref

    return render(request, 'vehicle_log/line_log.htm', {
        'title': 'Linje %s' % line_obj,
        'line_obj': line_obj,
        'vehicles': vehicles_obj.items(),
        'logs': logs,
    })


def block_ref_log(request, block_ref):
    logs = VehicleLog.objects.filter(
        block_ref=block_ref,
        origin_departure_time__year=year).select_related(
        'line', 'vehicle_type', 'operator', 'vehicle_type__operator', 'origin',
        'origin__Stop', 'destination')
    return render(request, 'vehicle_log/block_ref_log.html',
                  {'logs': logs, 'title': 'Vognløp %s' % block_ref})


def operator(request, prefix=None):
    if not prefix:
        return render(request, 'vehicle_log/operators.html',
                      {'operators': Operator.objects.all()})

    operator_id = prefix
    operator_obj = Operator.objects.get(vehicle_prefix=operator_id)

    unknown_last_seen = VehicleLog.objects.prefetch_related('line').raw(
        'SELECT item_id,vehicle_ref,line_id,'
        'max(origin_departure_time) AS origin_departure_time '
        'FROM vehicle_log_vehiclelog WHERE operator_id=%s AND '
        'vehicle_type_id IS NULL GROUP BY vehicle_ref ORDER BY vehicle_ref',
        [operator_obj.id])

    return render(request, 'vehicle_log/operator.html',
                  {'operator': operator_obj,
                   'unknown': unknown_last_seen,
                   'title': operator_obj.name_string()})


def vehicle_type(request, key):
    vehicle_obj = Vehicle.objects.get(id=key)

    low, high = vehicle_obj.numbers()
    vehicle_last_seen = VehicleLog.objects.prefetch_related('line').raw(
        'SELECT item_id,max(origin_departure_time) AS origin_departure_time,'
        'vehicle_ref,line_id '
        'FROM vehicle_log_vehiclelog '
        'WHERE vehicle_ref>=%s AND vehicle_ref<=%s '
        'GROUP BY vehicle_ref ORDER BY vehicle_ref',
        [low, high])

    return render(request, 'vehicle_log/vehicle_type.html',
                  {'vehicle': vehicle_obj, 'last_seen': vehicle_last_seen})


def index(request):
    return render(request, 'vehicle_log/index.html')
