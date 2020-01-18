class VehicleInfo:
    @staticmethod
    def info(vehicle_id):
        from vehicle_type.models import Vehicle
        prefix, vehicle_id = VehicleInfo.parse_number(vehicle_id)

        if prefix:
            info = Vehicle.objects.filter(numlow__lte=vehicle_id, num_prefix=prefix)
            info = info.get(numhigh__gte=vehicle_id, num_prefix=prefix)
        else:
            info = Vehicle.objects.filter(numlow__lte=vehicle_id)
            info = info.get(numhigh__gte=vehicle_id)
        return info

    @staticmethod
    def parse_number(number, prefix=None):
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
