from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from pricecompare.models import ContactForm
from django.template import RequestContext, Context
from django import forms as forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError

from decimal import Decimal

from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from pricecompare.models import (State, IndustryGroup, LossCost, ClassCode,
                                 CarrierState, StateModifier, Carrier)

class ContactView(TemplateView):
    template_name = "contact.html"

    def contactview(request):
        subject = request.POST.get('topic', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['brian@compmatrix.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thankyou/')
        else:
            return render_to_response('contact.html', {'form': ContactForm()})

        return render_to_response('contact.html', {'form': ContactForm()},
                            RequestContext(request))

    def thankyou(request):
        return render_to_response('thankyou.html')


class HomeView(TemplateView):
    template_name = "home.html"

class ThankYou(TemplateView):
    template_name = "thankyou.html"


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = {
            'states': State.objects.filter(active=True).order_by('name'),
            'industries': IndustryGroup.objects.all(),
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

        loss_cost = LossCost.objects.filter(class_code__code=form_class_code, state__abbreviation=carrier_state.state.abbreviation)[:1].get()

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

        loss_cost = LossCost.objects.filter(class_code__code=form_class_code, state__abbreviation=state_abbr)[:1].get()

        for carrier_state in carrier_states:
            carrier_state.set_inputs(loss_cost, payroll, mod)

        return_val.context_data['carrier_states'] = carrier_states
        return_val.context_data['loss_cost'] = loss_cost
        return_val.context_data['payroll'] = payroll
        return_val.context_data['mod'] = mod
        return_val.context_data['state'] = request.GET.get('state')

        return return_val

