from vehicle_type.models import Operator, Vehicle


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
        vehicle_prefix=prefix, defaults={'name': name})
    return operator


def vehicle_type(number: int = None, operator: Operator = None,
                 prefix: int = None,
                 prefixed_number: int = None) -> Vehicle:
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
