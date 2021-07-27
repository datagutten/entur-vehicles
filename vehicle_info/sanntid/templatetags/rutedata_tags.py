from django import template
from rutedata.models import Line, Quay

register = template.Library()


def line_name(line_ref):
    try:
        line = Line.objects.get(id=line_ref)
        return '%s %s' % (line.PublicCode, line.Name)
    except Line.DoesNotExist:
        return line_ref


register.filter('line_name', line_name)


def quay_name(quay_ref):
    try:
        quay = Quay.objects.get(id=quay_ref)
        if not quay.Description:
            return quay.Stop.Name
        else:
            return '%s (%s)' % (quay.Stop.Name, quay.Description)
    except Quay.DoesNotExist:
        return quay_ref


register.filter('quay_name', quay_name)
