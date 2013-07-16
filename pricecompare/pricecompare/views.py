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
        if not compares:
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


class DetailView(TemplateView):
    template_name = "carrier_view.html"

    def get_context_data(self, **kwargs):
        carrier_state_id = kwargs.get('carrier_state_id', None)
        carrier_state = CarrierState.objects.get(id=carrier_state_id)

        payroll = self.request.GET.get('payroll_1')
        form_class_code = self.request.GET.get('class_code_1')
        mod = Decimal(self.request.GET.get('mod'))

        loss_cost = LossCost.objects.get(class_code__code=form_class_code, state__abbreviation=carrier_state.state.abbreviation)

        carrier_state.set_inputs(loss_cost, payroll, mod)
        context = {
            'carrier_state': carrier_state,
            'mod': mod,
            'loss_cost': loss_cost, 
            'payroll': payroll
        }
        return context

class CompareView(TemplateView):
    template_name = "compare.html"
    def get(self, request, *args, **kwargs):
        return_val = super(CompareView, self).get(request, *args, **kwargs)
        compares = request.GET.getlist('compare[]')

        mod = Decimal(request.GET.get('mod'))
        payroll = request.GET.get('payroll_1')
        form_class_code = request.GET.get('class_code_1')
        state_abbr = request.GET.get('state')

        carrier_states = CarrierState.objects.filter(id__in=compares)
        loss_cost = LossCost.objects.get(class_code__code=form_class_code, state__abbreviation=state_abbr)

        for carrier_state in carrier_states:
            carrier_state.set_inputs(loss_cost, payroll, mod)

        return_val.context_data['carrier_states'] = carrier_states
        return_val.context_data['loss_cost'] = loss_cost
        return_val.context_data['payroll'] = payroll
        return_val.context_data['mod'] = mod
        return_val.context_data['state'] = state_abbr

        return return_val
   

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

        loss_cost = LossCost.objects.get(class_code__code=form_class_code, state__abbreviation=state_abbr)

        for carrier_state in carrier_states:
            carrier_state.set_inputs(loss_cost, payroll, mod)

        return_val.context_data['carrier_states'] = carrier_states
        return_val.context_data['loss_cost'] = loss_cost
        return_val.context_data['payroll'] = payroll
        return_val.context_data['mod'] = mod
        return_val.context_data['state'] = request.GET.get('state')

        return return_val

