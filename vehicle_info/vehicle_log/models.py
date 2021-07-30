from django.db import models

from rutedata.models import Line, Quay
from vehicle_type import info
from vehicle_type.models import Operator, Vehicle


class VehicleLog(models.Model):
    item_id = models.CharField(max_length=200, primary_key=True, blank=False)
    line_ref = models.CharField(max_length=200)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, blank=True,
                             null=True, related_name='vehicles')
    block_ref = models.CharField(max_length=200)
    vehicle_ref = models.IntegerField(db_index=True)
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

    class Meta:
        ordering = ['-origin_departure_time']

    def __str__(self):
        if self.line:
            line = self.line
        else:
            line = self.line_ref

        return '%s %s %s' % (line, self.operator_ref,
                             self.vehicle_ref)

    def vehicle_num(self):
        if not self.operator or not self.vehicle_type:
            return self.vehicle_ref
        else:
            prefix, number = info.split_number(self.vehicle_ref, self.operator.vehicle_prefix)
            return number

    def find_vehicle_type(self):
        if self.vehicle_type:
            return self.vehicle_type
        else:
            return info.vehicle_type(prefixed_number=self.vehicle_ref,
                                     operator=self.operator)
