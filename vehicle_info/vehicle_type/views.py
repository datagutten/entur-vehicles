import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from . import info
from .models import ExpectedVehicle, Vehicle


def index(request):
    return HttpResponse("Hello, world. You're at the vehicles index.")


def vehicle_info(request, vehicle_id):
    try:
        vehicle = info.vehicle_type(prefixed_number=vehicle_id)
    except ObjectDoesNotExist:
        return HttpResponse('Ukjent internnummer: %d' % vehicle_id)

    return render(request, 'vehicle_type/vehicle.html', {'vehicle': vehicle, 'vehicle_id': vehicle_id})


def info_json(request, vehicle_id):
    try:
        prefix, number = info.split_number(vehicle_id)
        vehicle = info.vehicle_type(number, prefix=prefix)

        data = {'operator': vehicle.operator.name_string(),
                'type': vehicle.type,
                'length': vehicle.length,
                'year': vehicle.year,
                'number': number,
                'string': str(vehicle),
                'error': '',
                }
    except ObjectDoesNotExist:
        data = {'error': 'Ukjent internnummer: %d' % vehicle_id}
    return HttpResponse(json.dumps(data))


def vehicle_expected(request, line_number, vehicle_number):
    try:
        vehicle = info.vehicle_type(prefixed_number=vehicle_number)
        ExpectedVehicle.objects.filter(vehicle=vehicle).get(line=line_number)
    except Vehicle.DoesNotExist:
        return HttpResponse('Ukjent internnummer: ' + str(vehicle_number))
    except ExpectedVehicle.DoesNotExist:
        return HttpResponse('%s er ikke forventet på linje %s' % (info, line_number))

    return HttpResponse(str(vehicle))
