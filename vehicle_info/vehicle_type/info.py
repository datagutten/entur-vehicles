from vehicle_type.models import Operator, Vehicle


class VehicleInfo:
    @staticmethod
    def info(vehicle_id):
        from vehicle_type.models import Vehicle
        prefix, vehicle_id = VehicleInfo.parse_number(vehicle_id)
        vehicle = Vehicle.objects.select_related('operator')

        if prefix:
            info = vehicle.filter(numlow__lte=vehicle_id, num_prefix=prefix)
            info = info.get(numhigh__gte=vehicle_id, num_prefix=prefix)
        else:
            info = vehicle.filter(numlow__lte=vehicle_id)
            info = info.get(numhigh__gte=vehicle_id)
        return info

    @staticmethod
    def parse_number(number, prefix=None):
        return split_number(number, prefix)

    @staticmethod
    def seen_on(number):
        from vehicle_log.models import VehicleLog
        log = VehicleLog.objects.filter(vehicle_ref=number)
        lines = log.values('line').distinct().order_by('line')
        return lines


def split_number(number, prefix=None):
    if prefix:
        prefix_length = len(str(prefix))
        number = str(number)
        number = int(number[prefix_length:])
    else:
        if len(str(number)) < 5:
            return None, number
        number = str(number)
        prefix = int(number[0:2])
        number = int(number[2:])
    return prefix, number


def get_operator(name, prefix):
    operator, created = Operator.objects.get_or_create(
        name=name,
        vehicle_prefix=prefix)
    return operator


def vehicle_type(number=None, operator=None, prefix=None,
                 prefixed_number=None):
    vehicle = Vehicle.objects.select_related('operator')
    if prefixed_number:
        prefix, number = split_number(prefixed_number)
    elif not number:
        raise AttributeError('Number or prefixed number must be set')

    if operator:
        return vehicle.get(numlow__lte=number, numhigh__gte=number,
                           operator=operator)
    elif prefix:
        return vehicle.get(numlow__lte=number, numhigh__gte=number,
                           operator__vehicle_prefix=prefix)
    else:
        raise AttributeError('Operator or prefix must be set')
