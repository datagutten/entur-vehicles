from django import template
from rutedata.models import Line, Quay

register = template.Library()
quay_cache = {}

def line_name(line_ref):
    try:
        line = Line.objects.get(id=line_ref)
        return '%s %s' % (line.PublicCode, line.Name)
    except Line.DoesNotExist:
        return line_ref


register.filter('line_name', line_name)


def quay_name(quay_ref):
    if quay_ref in quay_cache:
        return quay_cache[quay_ref].Stop.Name

    try:
        quay = Quay.objects.select_related('Stop').get(id=quay_ref)
        quay_cache[quay_ref] = quay
        if not quay.Description or quay.Description == quay_ref:
            return quay.Stop.Name
        else:
            return '%s (%s)' % (quay.Stop.Name, quay.Description)
    except Quay.DoesNotExist:
        return quay_ref


register.filter('quay_name', quay_name)
