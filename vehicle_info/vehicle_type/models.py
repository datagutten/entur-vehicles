from django.db import models
from vehicle_log.models import VehicleLog


class Operator(models.Model):
    name = models.CharField(max_length=60)
    vehicle_prefix = models.IntegerField()

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    numlow = models.IntegerField('Internnummer fra')
    numhigh = models.IntegerField('Internnummer til')
    type = models.CharField('Type/modell', max_length=200, blank=True, default='')
    length = models.IntegerField('Lengde', blank=True, default=0)
    year = models.IntegerField('Årsmodell', blank=True, default=0)
    fuel = models.CharField('Drivstoff', max_length=200, blank=True, default='')
    num_prefix = models.IntegerField('Ekstra sifer foran internnummer', blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT, verbose_name='Operatør')

    def __str__(self):
        if self.length > 0:
            length = str(self.length) + 'm '
        else:
            length = ''
        if self.year > 0:
            year = ' ' + str(self.year)
        else:
            year = ''
        return str(self.operator) + ' ' + str(self.numlow) + '-' + str(self.numhigh) + ' ' + str(self.type) + ' ' + length + year

    def seen_on(self):
        prefix = self.operator.vehicle_prefix * 10000
        # print(prefix + self.numlow)
        log = VehicleLog.objects.filter(vehicle_ref__gte=prefix + self.numlow, vehicle_ref__lte=prefix + self.numhigh)
        lines = log.values('line').distinct().order_by('line')
        return lines

    def seen_on_links(self):
        from rutedata.models import Line

        lines = ''
        for line_id in self.seen_on():
            lines += "%s\n" % Line.objects.get(id=line_id['line'])

        return lines

    def numlow_noprefix(self):
        if self.num_prefix:
            return self.numlow - (self.num_prefix*1000)
        else:
            return self.numlow

    def numhigh_noprefix(self):
        if self.num_prefix:
            return self.numhigh - (self.num_prefix*1000)
        else:
            return self.numhigh

    class Meta:
        ordering = ['numlow']


class ExpectedVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    line = models.CharField('Linje materiellet brukes på', max_length=5)

    class Meta:
        ordering = ['line']

    def __str__(self):
        return self.line + ": " + str(self.vehicle)
