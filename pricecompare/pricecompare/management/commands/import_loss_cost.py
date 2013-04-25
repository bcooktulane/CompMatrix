import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("/tmp/lost_cost.csv","rb"))
        row_count = 0
        for row in cr:
            print row_count
            row_count += 1
            (state, code, name, group) = row[0:4]
   
            try:
                loss = Decimal(row[12])
            except Exception as e:
                print e
                loss = 0 

            code = int(code)
            name = name.strip()

            state = State.objects.get(name=state.strip())
            industry = IndustryGroup.objects.get(name=group)
            

            class_code, created = ClassCode.objects.get_or_create(
                code=code,
                industry_group=industry,
                name=name
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
