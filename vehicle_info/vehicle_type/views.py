from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from vehicle_type.info import VehicleInfo

from .models import Vehicle, ExpectedVehicle


def index(request):
    return HttpResponse("Hello, world. You're at the vehicles index.")


def vehicle_info(request, vehicle_id):
    # return HttpResponse("You're looking at vehicle %s." % vehicle_id)
    try:
        info = Vehicle.objects.filter(numlow__lte=vehicle_id)
        info = info.get(numhigh__gte=vehicle_id)
    except Vehicle.DoesNotExist:
        return False
    return info


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
