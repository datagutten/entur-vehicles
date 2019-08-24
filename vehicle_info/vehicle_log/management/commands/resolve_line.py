from django.core.management.base import BaseCommand
from vehicle_log.models import VehicleLog
from rutedata.models import Line


class Command(BaseCommand):
    help = 'Import lines from XML'

    def handle(self, *args, **options):
        log = VehicleLog.objects.filter(line=None)
        for entry in log.all():
            try:
                print(entry)
                line = Line.objects.get(id=entry.line_ref)
                print(line)
                entry.line = line
                entry.save()
            except Line.DoesNotExist as e:
                print('Line not found: %s' % entry.line_ref)
                continue
            # break
