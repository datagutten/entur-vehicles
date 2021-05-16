import re

import dateutil.parser
from django import template
from django.core.exceptions import ObjectDoesNotExist

from vehicle_type import info

register = template.Library()


def time(value):
    try:
        return dateutil.parser.parse(value).strftime('%H:%M')
    except ValueError:
        return value


register.filter('time', time)


def color(line):
    """Show line color
    colors.json is generated from entur static data"""

    import json
    import os
    import re
    matches = re.match(r'([A-Z]+:Line:[0-9A-Z]+).*', line)
    if matches:
        line = matches.group(1)

    try:
        fp = open(os.path.dirname(__file__) + '/colors.json')
        colours = json.load(fp)
        if line in colours:
            return '#' + colours[line]
        else:
            return 'none'
    except FileNotFoundError:
        return 'none'


register.filter('color', color)


def dest_text(dest):
    import re
    matches = re.match(r'[A-Z]+:Line:[0-9A-Z]+(.+)', dest)
    if matches:
        return matches.group(1)
    else:
        return ''


register.filter('dest_text', dest_text)


def line_num(dest):
    matches = re.match(r'[A-Z]+:Line:([0-9A-Z]+).*', dest)
    if matches:
        return matches.group(1)
    else:
        return ''


register.filter('line_num', line_num)


def line_id(dest):
    matches = re.match(r'([A-Z]+:Line:[0-9A-Z]+).*', dest)
    if matches:
        return matches.group(1)
    else:
        return ''


register.filter('line_id', line_id)


def parse_time(string):
    import dateutil.parser
    try:
        return dateutil.parser.parse(string)
    except ValueError:
        return string


def delay(departure):
    from sanntid import utils
    expected = parse_time(departure['expectedDepartureTime'])
    aimed = parse_time(departure['aimedDepartureTime'])

    if expected > aimed:  # Delayed
        diff = expected - aimed
        prefix = '-'
    else:  # Early
        diff = aimed - expected
        prefix = '+'

    if diff.seconds < 15:
        # print('Delay is %d seconds' % diff.seconds)
        return None
    # print(diff)
    # print(diff.seconds)

    return prefix + utils.delay_string(diff.seconds)


register.filter('delay', delay)


def split_number(number):
    prefix, number_split = info.split_number(number)
    if not prefix:
        return number

    try:
        vehicle = info.vehicle_type(number_split, prefix=prefix)
        return '%d-%d' % (vehicle.operator.vehicle_prefix, number_split)
    except ObjectDoesNotExist:
        return number


register.filter('split_number', split_number)
