import re
import xml.etree.ElementTree

from django.core.management.base import BaseCommand
from vehicle_log.models import VehicleLog

from datetime import datetime
from entur_api.siri import Siri
from rutedata.models import Line


class Command(BaseCommand):
    help = 'Import lines from XML'

    def handle(self, *args, **options):
        data = Siri('datagutten-vehicle-log')
        activities = data.vehicle_activities()
        for activity in activities:
            log = VehicleLog(line_ref=activity.line_ref(),
                             block_ref=activity.block_ref(),
                             vehicle_ref=activity.vehicle(),
                             item_id=activity.find('.//siri:ItemIdentifier'),
                             origin_quay_ref=activity.origin_ref(),
                             origin_departure_time=activity.origin_time(),
                             operator_ref=activity.operator())
            try:
                line = Line.objects.get(id=activity.line_ref())
                log.line = line
            except Line.DoesNotExist:
                pass

            log.save()
