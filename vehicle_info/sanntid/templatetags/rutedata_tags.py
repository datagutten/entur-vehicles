from django import template
from rutedata.models import Line, Quay
from typing import Optional

register = template.Library()
quay_cache = {}

def line_name(line_ref):
    try:
        line = Line.objects.get(id=line_ref)
        return '%s %s' % (line.PublicCode, line.Name)
    except Line.DoesNotExist:
        return line_ref


register.filter('line_name', line_name)


def quay(quay_ref) -> Optional[Quay]:
    if quay_ref in quay_cache:
        return quay_cache[quay_ref]
    try:
        quay_obj = Quay.objects.select_related('Stop').get(id=quay_ref)
        quay_cache[quay_ref] = quay_obj
        return quay_obj
    except Quay.DoesNotExist:
        return None


def quay_stop_name(quay_ref):
    quay_obj = quay(quay_ref)
    if not quay_obj or not quay_obj.Stop:
        return quay_ref

    if quay_ref in quay_cache:
        return quay_cache[quay_ref].Stop.Name

    try:
        if not quay_obj.Description or quay_obj.Description == quay_ref:
            return quay_obj.Stop.Name
        else:
            return '%s (%s)' % (quay_obj.Stop.Name, quay_obj.Description)
    except Quay.DoesNotExist:
        return quay_ref


def quay_name(quay_ref):
    quay_obj = quay(quay_ref)
    if not quay_obj:
        return quay_ref
    if quay_obj.Description:
        description = quay_obj.Description
    elif quay_obj.Stop.Description:
        description = quay_obj.Stop.Description
    else:
        description = ''

    return ('%s %s' % (
        quay_obj.PublicCode or '', description)).strip()


register.filter('quay_name', quay_name)
register.filter('quay_stop_name', quay_stop_name)
