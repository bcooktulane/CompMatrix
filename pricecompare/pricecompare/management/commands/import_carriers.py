import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("/tmp/carriers.csv","rb"))
        row_count = 0
        for row in cr:
            print row_count
            row_count += 1
            (state, code, group, name, premium) = row[0:5]
            if state == "State":
                continue
            lcm = row[10]
            premium = premium.replace('$','').replace(',','').strip()
            if premium == "N/A":
                premium=None
            elif '(' in premium:
                premium = Decimal(premium.replace('(', '').replace(')',''))
                premium = -premium
                print premium

            code = int(code)
            group = int(group)
            name = name.strip()

            state = State.objects.get(name=state.strip())
            carrier, created = Carrier.objects.get_or_create(
                code=code, group=group)
            if created:
                carrier.name = name
                carrier.save()
                print "create carrier"

            try:
                carrier_state = CarrierState.objects.get(
                    state=state,
                    carrier=carrier)
                print "Found %s" % carrier
            except CarrierState.DoesNotExist:
                carrier_state = CarrierState(
                    state=state,
                    carrier=carrier,
                    premium=premium,
                    lcm = lcm)
                carrier_state.save()
                print "created carrier state"

