from django import template
from rutedata.models import Line

register = template.Library()


def line_name(line_ref):
    try:
        line = Line.objects.get(id=line_ref)
        return '%s %s' % (line.PublicCode, line.Name)
    except Line.DoesNotExist:
        return line_ref


register.filter('line_name', line_name)

