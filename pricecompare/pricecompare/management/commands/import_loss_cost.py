import csv
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from pricecompare.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        cr = csv.reader(open("/vagrant/import_data/loss_cost.csv","rb"))
        row_count = 0
        for row in cr:
            row_count += 1
            (state, code, loss) = row[0:3]

            green_flags = row[17:22]
            yellow_flags = row[22:28]
            red_flags = row[28:33]
   
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

            for flag in green_flags:
                if flag and flag != "0":
                    flag_obj, flag_created = ClassFlag.objects.get_or_create(description=flag, flag_color="green")
                    if not loss_cost.flags.filter(id=flag_obj.id).count():
                        loss_cost.flags.add(flag_obj)
                    if flag_created:
                        print "Created flag %s" % flag

            for flag in red_flags:
                if flag and flag != "0":
                    flag_obj, flag_created = ClassFlag.objects.get_or_create(description=flag, flag_color="red")
                    if not loss_cost.flags.filter(id=flag_obj.id).count():
                        loss_cost.flags.add(flag_obj)
                    if flag_created:
                        print "Created flag %s" % flag

            for flag in yellow_flags:
                if flag and flag != "0":
                    flag_obj, flag_created = ClassFlag.objects.get_or_create(description=flag, flag_color="yellow")
                    if not loss_cost.flags.filter(id=flag_obj.id).count():
                        loss_cost.flags.add(flag_obj)
                    if flag_created:
                        print "Created flag %s" % flag
