from django import db
from django.core.management.base import BaseCommand

from entur_api.siri import Siri
from rutedata.models import Line, Quay
from vehicle_log.models import VehicleLog
from vehicle_type import info
from vehicle_type.models import Vehicle


class Command(BaseCommand):
    help = 'Import lines from XML'

    def handle(self, *args, **options):
        data = Siri('datagutten-vehicle-log')
        activities = data.vehicle_activities()
        for activity in activities:
            try:
                origin, created = Quay.objects.get_or_create(
                    id=activity.origin_ref())
            except db.Error as e:
                print(e)
                origin = None

            try:
                destination, created = Quay.objects.get_or_create(
                    id=activity.destination_ref())
            except db.Error as e:
                print(e)
                destination = None

            prefix, number = info.split_number(activity.vehicle())

            operator = None
            vehicle_type = None
            if prefix:
                try:
                    operator = info.get_operator(activity.operator(), prefix)
                except db.Error as e:
                    print(e)

                if operator:
                    try:
                        vehicle_type = info.vehicle_type(number, operator)
                    except Vehicle.DoesNotExist:
                        pass

            log = VehicleLog(line_ref=activity.line_ref(),
                             block_ref=activity.block_ref(),
                             vehicle_ref=activity.vehicle(),
                             item_id=activity.find('.//siri:ItemIdentifier'),
                             origin_quay_ref=activity.origin_ref(),
                             origin_departure_time=activity.origin_time(),
                             operator_ref=activity.operator(),
                             operator=operator,
                             vehicle_type=vehicle_type,
                             origin=origin,
                             destination=destination,
                             )
            try:
                line = Line.objects.get(id=activity.line_ref())
                log.line = line
            except Line.DoesNotExist:
                pass

            log.save()
