import re
import xml.etree.ElementTree
from datetime import datetime

from django.core.management.base import BaseCommand
from rutedata.load_xml.LoadLines import LoadLines
from rutedata.load_xml.load_xml import LoadXml
from sanntid.models import EndStops


class Command(BaseCommand):
    help = 'Import lines from XML'

    def handle(self, *args, **options):
        # Lines
        line_filter = None

        load = LoadLines()

        zip_file = load.load_netex(None)
        for file in zip_file.namelist():
            if file.find('RUT_RUT-Line') == -1:
                continue
            if line_filter and file.find(line_filter) == -1:
                continue

            print(file)
            xml_bytes = zip_file.read(file)
            root = xml.etree.ElementTree.fromstring(xml_bytes)
            journeys = root.findall(
                './/netex:frames/netex:TimetableFrame/netex:vehicleJourneys/netex:ServiceJourney',
                load.namespaces)
            for journey in journeys:
                print(journey)
                journey_id = journey.get('id')
                print(journey_id)
                if journey_id is None:
                    print('Missing journey id')
                    break
                helper = LinePassingHelper2(xml_root=root, service_journey_id=journey_id)
                first_passing = helper.first_passing()
                last_passing = helper.last_passing()

                print(helper.first_quay())
                print(helper.last_quay())

                first_departure_time = first_passing.find('./netex:DepartureTime', helper.namespaces)
                first_departure_time = first_departure_time.text
                print(first_departure_time)
                first_departure_time_time = datetime.strptime(first_departure_time, '%H:%M:%S')

                last_departure_time = last_passing.find('./netex:ArrivalTime', helper.namespaces)
                last_departure_time = last_departure_time.text
                last_departure_time_time = datetime.strptime(last_departure_time, '%H:%M:%S')

                db = EndStops(first_quay=helper.first_quay(), last_quay=helper.last_quay(),
                              first_passing=first_departure_time_time,
                              last_passing=last_departure_time_time, service_journey_id=journey_id, line_id_string=file
                              )
                db.save()


class LinePassingHelper2(LoadXml):
    def __init__(self, xml_root, service_journey_id):
        self.root = xml_root
        self.passings = self.find_passings(service_journey_id,
                                           xml_root=self.root)

    def get_quay(self, passing):
        stop_point_id = self.get(passing, 'StopPointInJourneyPatternRef')
        point_id = self.stop_point(stop_point_id=stop_point_id,
                                   xml_root=self.root)
        quay_id = re.sub(r'.*default-([0-9]+)', r'NSR:Quay:\1', point_id)
        return quay_id

    def first_passing(self):
        return self.passings[0]

    def last_passing(self):
        return self.passings[-1]

    def first_quay(self):
        return self.get_quay(self.first_passing())

    def last_quay(self):
        return self.get_quay(self.last_passing())

    def passing_time(self, passing):
        return passing.find('./netex:DepartureTime', self.namespaces)
