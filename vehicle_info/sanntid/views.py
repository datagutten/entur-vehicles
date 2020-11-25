from pprint import pprint

import dateutil.parser
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from entur_api.geocoder import GeoCoder
from entur_api.journey_planner import EnturApi
from entur_api.siri import Siri
from sanntid.models import EndStops
from rutedata.models import Stop

entur = EnturApi('datagutten-sanntidpluss')
geocoder = GeoCoder('datagutten-sanntidpluss')


def origin_departure_time(departure):
    journey_id = departure['serviceJourney']['id']
    line_id = departure['serviceJourney']['journeyPattern']['line']['id']
    try:
        end_db = EndStops.objects.get(service_journey_id=journey_id)

        date = dateutil.parser.parse(departure['aimedDepartureTime'])
        combined = date.combine(date, end_db.first_passing, tzinfo=date.tzinfo)
        return [end_db.first_quay, combined.isoformat()]
    except EndStops.DoesNotExist:
        print('Missing %s' % journey_id)
        return [None, None]


def vehicle_data(departure):
    line = departure['serviceJourney']['journeyPattern']['line']['id']
    entur_siri = Siri('datagutten-sanntidpluss', line=line)
    # [origin_departure, origin_time] = origin_departure_time(departure)
    [origin_quay, origin_time] = origin_departure_time(departure)
    if origin_time is not None:
        try:
            return entur_siri.find_vehicle_activity(
                origin_time,
                line=line,
                origin_quay=origin_quay)  # origin_quay=origin_departure.point.quay.id)
        except AttributeError:
            print('Departure %s not found' % origin_time)
            try:
                entur_siri.find_vehicle_activity(
                    origin_time, line=line,
                    origin_quay=origin_quay, debug=True)  # origin_departure.point.quay.id)
            except AttributeError:
                pass


def get_stop_departures(stop):
    departures = entur.stop_departures_app(stop, 20)
    departures_sorted = dict()
    for departure in departures['data']['stopPlace']['estimatedCalls']:
        if not departure['realtime']:
            continue
        print('Origin: ', origin_departure_time(departure))
        # print(departure['realtime'])
        quay_id = departure['quay']['id']
        dest = '%s %s' % (
                departure['serviceJourney']['journeyPattern']['line']['id'],
                departure['destinationDisplay']['frontText'])

        departure['vehicle'] = vehicle_data(departure)

        if quay_id not in departures_sorted:
            departures_sorted[quay_id] = dict()
        if dest not in departures_sorted[quay_id]:
            departures_sorted[quay_id][dest] = []

        departures_sorted[quay_id][dest].append(departure)
    return departures_sorted


def get_quay_departures():
    pass


def stop_departures(request, stop):
    departures_sorted = get_stop_departures(stop)
    try:
        stop_info = Stop.objects.get(id=stop)
        stop_name = stop_info.Name
    except Stop.DoesNotExist:
        stop_name = stop

    return render(request, 'sanntid/departures.html', {'departures': departures_sorted, 'title': stop_name})


def select_stop(request):
    return render(request, 'sanntid/find_stop.html')


def stops_latlon(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')
    print(latitude, longitude)
    url = 'https://api.entur.io/geocoder/v1/reverse?point.lat=%s&point.lon=%s&lang=en&size=10&layers=venue' \
          % (latitude, longitude)
    print(url)
    # stops = geocoder.reverse(latitude, longitude)
    data = geocoder.get(url)
    stops = data['features']

    pprint(stops)

    context = {'stops': stops}
    return render(request, 'sanntid/stops.html', context=context)


def vehicle_status(request, line, line2=None):
    entur_siri = Siri('datagutten-sanntidpluss', line=line)
    activities = entur_siri.vehicle_activities()
    if line2 is not None:
        siri2 = Siri('datagutten-sanntidpluss', line=line2)
        activities2 = siri2.vehicle_activities()
        cols = request.GET.get('cols', 'false')
        if cols == 'false':
            return render(request, 'sanntid/activities2_list.html', {'activities1': activities, 'activities2': activities2})
        else:
            return render(request, 'sanntid/activities2.html', {'activities1': activities, 'activities2': activities2})
    else:
        activities2 = None
        return render(request, 'sanntid/activities.html', {'activities': activities})


def autocomplete(request):
    text = request.GET.get('text')
    data = geocoder.get(
        'https://api.entur.io/geocoder/v1/autocomplete?lang=no&layers=venue&boundary.county_ids=03,30&text=' + text)
    return render(request, 'sanntid/stops.html', context=
                  {'stops': data['features']})


def departures_json(request, stop=None, quay=None):
    if stop is not None:
        departures = entur.stop_departures_app(stop, 20)
        return JsonResponse(departures, safe=False)
