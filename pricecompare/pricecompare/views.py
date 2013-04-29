from decimal import Decimal

from django.shortcuts import redirect
from django.views.generic import TemplateView

from pricecompare.models import (State, IndustryGroup, LossCost, ClassCode,
                                 CarrierState)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        try:
            context = {
                'num_class_codes': range(len(self.request.session['class_codes'])),
                'states': State.objects.filter(active=True).order_by('name'),
                'industries': IndustryGroup.objects.all()
            }
        except:
            ## While changing things reset their session
            self.request.session.flush()
        return context


class QuoteView(TemplateView):
    template_name = "quote.html"

    def post(self, request, *args, **kwargs):
        # Get the loss cost
        class_codes = []

        for var in request.POST:
            if 'class_code_' in var:
                num = var.replace('class_code_', '')
                class_code = request.POST.get(var)
                payroll = request.POST.get('payroll_%s' % num)
                payroll = Decimal(payroll)
                try:
                    state = State.objects.get(abbreviation=request.POST.get('state'))
                    code = ClassCode.objects.get(code=class_code)
                    loss = LossCost.objects.get(class_code=code, state=state)
                    class_codes.append({
                        'class_code': class_code,
                        'payroll': payroll,
                        'code': code,
                        'state': state,
                        'loss': loss,
                    })
                except State.DoesNotExist:
                    raise AssertionError("State does not exist")
                except ClassCode.DoesNotExist:
                    raise AssertionError("Class code does not exist")
                except LossCost.DoesNotExist:
                    raise AssertionError("LostCost not found")
                except TypeError:
                    print "Payroll is wrong"

        mod = Decimal(request.POST.get('mod'))

        # Get the carriers
        carriers = []
        for carrier in CarrierState.objects.filter(state=state):
            # Only if they have a premium > 0
            max = 0
            min = 0
            if not carrier.premium or carrier.premium <= 0:
                continue

            rates = {}
            for class_code in class_codes:
                rate = carrier.lcm * class_code['loss'].loss_cost
                print carrier
                print "   %s" % rate

                final = (payroll/100) * rate * mod
                if final > max:
                    max = final
                if min == 0 or final < min:
                    min = final
                rates.update({'rate': rate, 'final': final})

            carriers.append({
                'carrier': carrier,
                'class_codes': rates,
                'max': max,
                'min': min,
            })


        for c in carriers:
            print c['class_codes']

        request.session['carriers'] = carriers
        request.session['class_codes'] = class_codes
        request.session['form'] = request.POST

        return redirect('home')
