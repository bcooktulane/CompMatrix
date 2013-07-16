import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("/vagrant/import_data/states.csv","rb"))
        row_count = 0
        for row in cr:
            print row_count
            row_count += 1
            (state, loss, max_credit, max_debit) = row[0:4]
   
            terrorism_loss = Decimal(loss)

            state_obj, created = State.objects.get_or_create(name=state, abbreviation=state[0:2])
            state_obj.max_credit = Decimal(max_credit[:-1]) / 100
            state_obj.max_debit = Decimal(max_debit[:-1]) / 100
            state_obj.terrorism_loss = terrorism_loss
            state_obj.save()
