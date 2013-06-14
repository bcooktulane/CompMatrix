import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("/vagrant/import_data/loss_cost.csv","rb"))
        row_count = 0
        for row in cr:
            print row_count
            row_count += 1
            (state, code, loss) = row[0:3]
   
            try:
                loss = Decimal(loss)
            except Exception as e:
                print e
                loss = 0 

            code = int(code)

            state = State.objects.get(name=state.strip())
            #industry = IndustryGroup.objects.get(name=group)
            

            class_code, created = ClassCode.objects.get_or_create(
                code=code,
            )
            if created:
                print "created"

            loss_cost, created = LossCost.objects.get_or_create(
                state=state,
                class_code=class_code)
            if created:
                loss_cost.loss_cost = loss
                loss_cost.save()
                print "Loss cost created"
