import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("import_data/carriers.csv","rb"))
        row_count = 0
        for row in cr:
            print row_count
            row_count += 1
            (state, code, group, name, premium) = row[0:5]
            lcm = row[9]
            constant = row[11]

            premium = premium.replace('$','').replace(',','').strip()
            if premium == "N/A":
                premium=None
            elif '(' in premium:
                premium = Decimal(premium.replace('(', '').replace(')',''))
                premium = -premium
                print premium

            name = name.strip()
            constant = constant.replace('$', '').replace(',','')

            state = State.objects.get(name=state.strip())
            carrier, created = Carrier.objects.get_or_create(name=name)
            if created:
                print "created"
            print constant
            carrier.expense_constant = constant
            carrier.save()

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
