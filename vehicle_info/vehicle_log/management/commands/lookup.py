import re
import xml.etree.ElementTree

from django.core.management.base import BaseCommand
from vehicle_log.models import VehicleLog

from datetime import datetime
from entur_api.siri import Siri
from django.db.models import ObjectDoesNotExist


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('vehicle', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['vehicle'][0])
        vehicles = VehicleLog.objects.filter(vehicle_ref=options['vehicle'][0])
        try:
            print(vehicles.first().vehicle_type())
        except ObjectDoesNotExist:
            pass
        print(vehicles.values('line_ref').distinct())
