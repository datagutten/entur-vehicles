from django.db import models


class Operator(models.Model):
    name = models.CharField(max_length=60)
    display_name = models.CharField(max_length=60, blank=True, null=True)
    vehicle_prefix = models.IntegerField(unique=True)

    class Meta:
        ordering = ['display_name', 'name', 'vehicle_prefix']

    def __str__(self):
        return self.name
