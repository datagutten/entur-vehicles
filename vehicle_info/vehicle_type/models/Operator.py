from django.db import models


class Operator(models.Model):
    name = models.CharField(max_length=60)
    display_name = models.CharField(max_length=60, blank=True, null=True)
    vehicle_prefix = models.IntegerField(unique=True)

    class Meta:
        ordering = ['display_name', 'name', 'vehicle_prefix']

    def name_string(self):
        return self.display_name or self.name

    def vehicle_nums(self):
        nums = []
        for vehicle_type in self.vehicles.all():
            low, high = vehicle_type.numbers()
            nums += range(low, high + 1)
        return nums

    def __str__(self):
        return '%s (%s)' % (
            self.name_string(), self.vehicle_prefix)
