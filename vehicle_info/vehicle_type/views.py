import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from vehicle_type.info import VehicleInfo
from .models import ExpectedVehicle


def index(request):
    return HttpResponse("Hello, world. You're at the vehicles index.")


def vehicle_info(request, vehicle_id):
    try:
        vehicle = VehicleInfo.info(vehicle_id)
    except ObjectDoesNotExist:
        return HttpResponse('Ukjent internnummer: %d' % vehicle_id)

    return render(request, 'vehicle_type/vehicle.html', {'vehicle': vehicle, 'vehicle_id': vehicle_id})


def info_json(request, vehicle_id):
    try:
        vehicle = VehicleInfo.info(vehicle_id)
        data = {'operator': vehicle.operator.name,
                'type': vehicle.type,
                'length': vehicle.length,
                'year': vehicle.year,
                'number': vehicle.remove_prefix(vehicle_id),
                'string': str(vehicle),
                'error': '',
                }
    except ObjectDoesNotExist:
        data = {'error': 'Ukjent internnummer: %d' % vehicle_id}
    return HttpResponse(json.dumps(data))


def vehicle_info_string(request, vehicle_id):
    info = VehicleInfo.info(vehicle_id)
    if not info:
        return HttpResponse('Ukjent internnummer: ' + str(vehicle_id))
    else:
        return HttpResponse(str(info))


def vehicle_expected(request, line_number, vehicle_number):
    info = VehicleInfo.info(vehicle_number)
    if not info:
        return HttpResponse('Ukjent internnummer: ' + str(vehicle_number))
    try:
        excepted = ExpectedVehicle.objects.filter(vehicle_id=info.id).get(line=line_number)
    except ExpectedVehicle.DoesNotExist:
        return HttpResponse('%s er ikke forventet på linje %s' % (info, line_number))

    return HttpResponse(info)
