from django.core.management.base import BaseCommand
from core.models import CalgaryAddress
import json

street_type_mapping = {'AL': 'Alley', 'AV': 'Avenue',
                       'BA': 'Bay', 'BV': 'Boulevard',
                       'CA': 'Cape', 'CE': 'Centre', 'CI': 'Circle', 'CL': 'Close', 'CM': 'Common', 'CO': 'Court', 'CR': 'Crescent', 'CV': 'Cove',
                       'DR': 'Drive',
                       'GA': 'Gate', 'GD': 'Gardens', 'GR': 'Green', 'GV': 'Grove',
                       'HE': 'Heath', 'HI': 'Highway', 'HL': 'Hill', 'HT': 'Heights',
                       'IS': 'Island',
                       'LD': 'Landing', 'LI': 'Link', 'LN': 'Lane',
                       'ME': 'Mews', 'MR': 'Manor', 'MT': 'Mount',
                       'PA': 'Park', 'PH': 'Path', 'PL': 'Place', 'PR': 'Parade', 'PS': 'Passage', 'PT': 'Point', 'PY': 'Parkway', 'PZ': 'Plaza',
                       'RD': 'Road', 'RI': 'Rise', 'RO': 'Row',
                       'SQ': 'Square', 'ST': 'Street',
                       'TC': 'Terrace', 'TR': 'Trail',
                       'VI': 'Villas', 'VW': 'View',
                      #'WK': 'Walk', ### UNCLEAN DATA! Be careful. Watch your WKs
                       'WK': 'Walkway',
                       'WY': 'Way'}



class Command(BaseCommand):
    help = 'Import from $PROJECT_ROOT/addresses.json the addresses for the database.'
    def handle(self, *args, **kwargs):
        with open('addresses.json') as addresses:
            data = json.load(addresses)
            length = len(data['data'])
            counter = 0
            perc = 0
            for addr_row in data['data']:
                row_id = addr_row[0]
                address = addr_row[8]
                neighbourhood = addr_row[9]
                street_abbr = addr_row[10]
                quadrant = addr_row[11]
                ext = addr_row[13]
                lng = addr_row[15]
                lat = addr_row[16]
                long_street = street_type_mapping[street_abbr]
                CalgaryAddress.objects.create(address=address,
                                              quardrant=quadrant,
                                              street_type=street_abbr,
                                              nieghbourhood=neighbourhood,
                                              extention=ext,
                                              long_cord=lng,
                                              lat_cord=lat,
                                              row_id=row_id,
                                              long_street_type=long_street,
                                              long_address=address.replace(' ' + street_abbr + ' ', ' ' + long_street +' '))
                counter += 1
                perc = round((counter/length) * 100, 2)
                if counter % 1000 == 0:
                    print("{0}/{1} ({2}%)".format(counter, length, perc))
            # print 100% after done
            print("{0}/{1} ({2}%)".format(counter, length, perc))
