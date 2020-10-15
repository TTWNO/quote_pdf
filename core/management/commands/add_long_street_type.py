from django.core.management.base import BaseCommand
from core.models import CalgaryAddress

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        addresses = CalgaryAddress.objects.all()
        length = len(addresses)
        counter = 0
        perc = 0
        for addr in addresses:
            street_type = addr.street_type
            long_street_type = street_type_mapping[street_type]
            addr.long_street_type = long_street_type
            counter += 1
            perc = round((counter / length) * 100, 2)
            addr.save()
            print("{0}/{1} ({2}%)".format(counter, lenth, perc))