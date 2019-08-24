from django.db import models


class Line(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    Name = models.CharField(max_length=200, blank=True, null=True)
    TransportMode = models.CharField(max_length=200, blank=True, null=True)
    TransportSubmode = models.CharField(max_length=200, blank=True, null=True)
    PublicCode = models.CharField('Linjenummer', max_length=200,
                                  blank=True, null=True)
    OperatorRef = models.CharField('Operatør', max_length=200,
                                   blank=True, null=True)
    RepresentedByGroupRef = models.CharField(max_length=200,
                                             blank=True, null=True)
    Colour = models.CharField(max_length=200, blank=True, null=True)


class EndStops(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='stops', blank=True, null=True)
    line_id_string = models.CharField(max_length=200, db_index=True)
    service_journey_id = models.CharField(max_length=200, primary_key=True)
    first_quay = models.CharField(max_length=200)
    last_quay = models.CharField(max_length=200)
    first_passing = models.TimeField()
    last_passing = models.TimeField()
