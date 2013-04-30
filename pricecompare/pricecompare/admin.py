from django.contrib import admin

from pricecompare.models import *


class CarrierAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(State)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(IndustryGroup)
admin.site.register(ClassCode)
admin.site.register(LossCost)
admin.site.register(CarrierState)
admin.site.register(StateModifier)
