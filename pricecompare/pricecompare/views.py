from decimal import Decimal

from django.shortcuts import redirect
from django.views.generic import TemplateView

from pricecompare.models import (State, IndustryGroup, LossCost, ClassCode,
                                 CarrierState)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = {
            'states': State.objects.filter(active=True).order_by('name'),
            'industries': IndustryGroup.objects.all()
        }
        return context


class QuoteView(TemplateView):
    template_name = "quote.html"

    def post(self, request, *args, **kwargs):
        # Get the loss cost
        try:
            state = State.objects.get(abbreviation=request.POST.get('state'))
            code = ClassCode.objects.get(code=request.POST.get('class_code'))
            loss = LossCost.objects.get(class_code=code, state=state)
        except State.DoesNotExist:
            raise AssertionError()
        except ClassCode.DoesNotExist:
            raise AssertionError()
        except LossCost.DoesNotExist:
            raise AssertionError()

        # Get the carriers
        payroll = Decimal(request.POST.get('payroll'))
        mod = Decimal(request.POST.get('mod'))

        if not payroll or not mod:
            raise AssertionError()

        carriers = []
        for carrier in CarrierState.objects.filter(state=state):
            rate = carrier.lcm * loss.loss_cost
            final = (payroll/100) * rate * mod
            carriers.append({
                'carrier': carrier,
                'final': final,
                'rate': rate
            })

        request.session['carriers'] = carriers
        request.session['form'] = request.POST

        return redirect('home')
