from decimal import Decimal

from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from pricecompare.models import (State, IndustryGroup, LossCost, ClassCode,
                                 CarrierState, StateModifier, Carrier)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        try:
            num_class_codes = range(len(self.request.session['class_codes']))
        except:
            num_class_codes = []

        carrier_id = kwargs.get('carrier_id', None)
        compares = self.request.session.get('compares', None)

        carrier = None
        carrier_data = None
        if carrier_id:
            for c in self.request.session['carriers']:
                if c['carrier'].id == int(carrier_id):
                    carrier_data = c
                    carrier = c['carrier'].carrier

        compare_carriers = []
        if compares:
            for compare_id in compares.split(','):
                for c in self.request.session['carriers']:
                    if c['carrier'].id == int(compare_id):
                        carrier_data = c
                        carrier = c['carrier'].carrier

                compare_carriers.append({
                    'carrier': carrier,
                    'carrier_data': carrier_data,
                })

        for cc in compare_carriers:
            print cc['carrier_data']

        context = {
            'num_class_codes': num_class_codes,
            'states': State.objects.filter(active=True).order_by('name'),
            'industries': IndustryGroup.objects.all(),
            'carrier_id': carrier_id,
            'carrier': carrier,
            'carrier_data': carrier_data,
            'compare_carriers': compare_carriers,
        }
        return context


class CompareView(View):
    def get(self, request, *args, **kwargs):
        compares = request.GET.get('ids', '')
        request.session['compares'] = compares
        return redirect('home')
   

class QuoteView(TemplateView):
    template_name = "quote.html"

    def get(self, request, *args, **kwargs):
        return_val = super(QuoteView, self).get(request, *args, **kwargs)

        state_abbr = request.GET.get('state')
        mod = Decimal(request.GET.get('mod'))

        # TODO: multiple of these can be submitted
        payroll = request.GET.get('payroll_1')
        form_class_code = request.GET.get('class_code_1')

        carrier_states = CarrierState.objects.filter(state__abbreviation=state_abbr,
                                          state__losscost__class_code__code=form_class_code,
                                          premium__gt=0)

        state = State.objects.get(abbreviation=state_abbr)

        class_code = ClassCode.objects.get(code=form_class_code)
        state = class_code.states.get(abbreviation=state_abbr)
        loss_cost = LossCost.objects.get(class_code=class_code, state=state)

        for carrier_state in carrier_states:
            carrier_state.set_inputs(loss_cost, payroll, mod)

        return_val.context_data['carrier_states'] = carrier_states

        return return_val

