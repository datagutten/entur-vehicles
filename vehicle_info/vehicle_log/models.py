from django.db import models

from rutedata.models import Line, Quay
from vehicle_type.models import Operator, Vehicle


class VehicleLog(models.Model):
    item_id = models.CharField(max_length=200, primary_key=True, blank=False)
    line_ref = models.CharField(max_length=200)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, blank=True,
                             null=True, related_name='vehicles')
    block_ref = models.CharField(max_length=200)
    vehicle_ref = models.IntegerField()
    origin_quay_ref = models.CharField(max_length=20)
    origin_departure_time = models.DateTimeField()
    operator_ref = models.CharField(max_length=200)

    operator = models.ForeignKey(Operator, on_delete=models.PROTECT,
                                 blank=True, null=True)
    vehicle_type = models.ForeignKey(Vehicle, on_delete=models.PROTECT,
                                     blank=True, null=True)
    origin = models.ForeignKey(Quay, on_delete=models.PROTECT, blank=True,
                               null=True, related_name='origin_logs')
    destination = models.ForeignKey(Quay, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='destination_logs')

    def __str__(self):
        if self.line:
            line = self.line
        else:
            line = self.line_ref

        return '%s %s %s' % (line, self.operator_ref,
                             self.vehicle_ref)

    def find_vehicle_type(self):
        from vehicle_type.models import Vehicle
        from vehicle_type.info import VehicleInfo
        [prefix, number] = VehicleInfo.parse_number(self.vehicle_ref)
        # print('Number: %s Prefix: %s' % (number, prefix))
        try:
            return Vehicle.objects.get(numlow__lte=number, numhigh__gte=number,
                                       num_prefix=prefix)
        except Vehicle.DoesNotExist:
            pass
