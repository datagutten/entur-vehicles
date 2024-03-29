from django.db import models

from vehicle_type.models import Operator


class Vehicle(models.Model):
    numlow = models.IntegerField('Internnummer fra')
    numhigh = models.IntegerField('Internnummer til')
    type = models.CharField('Type/modell', max_length=200, null=True,
                            blank=True, default='')
    length = models.IntegerField('Lengde', null=True, blank=True, default=0)
    year = models.IntegerField('Årsmodell', null=True, blank=True, default=0)
    fuel = models.CharField('Drivstoff', max_length=200, null=True, blank=True,
                            default='')
    num_prefix = models.IntegerField('Ekstra sifer foran internnummer',
                                     blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT,
                                 verbose_name='Operatør', blank=True,
                                 null=True, related_name='vehicles')

    def numbers(self):
        low = int('%d%04d' % (self.operator.vehicle_prefix, self.numlow))
        high = int('%d%04d' % (self.operator.vehicle_prefix, self.numhigh))
        return low, high

    def last_seen(self):
        return self.logs.select_related('line').first()

    def first_seen(self):
        return self.logs.select_related('line').last()

    def name(self):
        if self.length and self.length > 0:
            length = str(self.length) + 'm '
        else:
            length = ''

        if self.year and self.year > 0:
            year = ' ' + str(self.year)
        else:
            year = ''

        return str(self.type) + ' ' + length + year

    def vehicle_prefix(self):
        if self.operator_id:
            return self.operator.vehicle_prefix

    def __str__(self):
        if self.length and self.length > 0:
            length = str(self.length) + 'm '
        else:
            length = ''
        if self.year and self.year > 0:
            year = ' ' + str(self.year)
        else:
            year = ''
        return str(self.operator) + ' ' + str(self.numlow) + '-' + str(self.numhigh) + ' ' + str(self.type) + ' ' + length + year

    class Meta:
        ordering = ['numlow']