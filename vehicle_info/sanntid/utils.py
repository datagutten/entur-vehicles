from datetime import datetime
import re
import dateutil.parser
import datetime


def parse_datetime(time):
    return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')


def seconds_fraction(seconds):

    if seconds == 0:
        return ''

    if seconds <= 15:
        return '¼'

    if seconds <= 30:
        return '½'

    if seconds <= 45:
        return '¾'

    if seconds > 45:
        return ''


def delay_string(seconds):
    minutes = int(seconds/60)
    seconds = seconds - (minutes*60)
    print('%d minutes, %d seconds' % (minutes, seconds))

    if seconds > 45:
        minutes += 1

    if minutes > 0:
        return '%d %s' % (minutes, seconds_fraction(seconds))
    else:
        return seconds_fraction(seconds)


def subst_time(date, time):
    time = str(time)
    date = re.match(r'([0-9\-]+T)[0-9:]+(\+[0-9]{2}).?([0-9]{2})', date)
    return date.group(1) + time + date.group(2) + ':' + date.group(3)


def combine_date_time(date, time):
    date = dateutil.parser.parse(date)
    if type(time) == str:
        time = datetime.datetime.strptime(time, '%H:%M:%S').time()
    date = date.combine(date, time, tzinfo=date.tzinfo)

    return date.isoformat()
