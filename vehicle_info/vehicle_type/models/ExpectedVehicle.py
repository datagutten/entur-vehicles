from django.db import models

from vehicle_type.models import Vehicle


class ExpectedVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    line = models.CharField('Linje materiellet brukes på', max_length=5)

    class Meta:
        ordering = ['line']

    def __str__(self):
        return self.line + ": " + str(self.vehicle)
