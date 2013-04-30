from decimal import Decimal

from django.shortcuts import redirect
from django.views.generic import TemplateView

from pricecompare.models import (State, IndustryGroup, LossCost, ClassCode,
                                 CarrierState, StateModifier)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        try:
            num_class_codes = range(len(self.request.session['class_codes']))
        except:
            num_class_codes = []

        carrier_id = kwargs.get('carrier_id', None)
        carrier = None
        carrier_data = None
        if carrier_id:
            for c in self.request.session['carriers']:
                if c['carrier'].id == int(carrier_id):
                    carrier_data = c
                    carrier = c['carrier'].carrier
                    print c['class_codes']

        context = {
            'num_class_codes': num_class_codes,
            'states': State.objects.filter(active=True).order_by('name'),
            'industries': IndustryGroup.objects.all(),
            'carrier_id': carrier_id,
            'carrier': carrier,
            'carrier_data': carrier_data
        }
        return context


class QuoteView(TemplateView):
    template_name = "quote.html"

    def get(self, request, *args, **kwargs):
        self.request.session.clear()
        return redirect('home')

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
            if not carrier.premium or carrier.premium <= 0:
                continue

            rates = []
            manual = 0
            total_payroll = 0
            total_premium = 0
            estimate = 0
            for class_code in class_codes:
                rate = carrier.lcm * class_code['loss'].loss_cost

                final = (class_code['payroll']/100) * rate * mod
                premium = (class_code['payroll']/100) * rate
                total_payroll += class_code['payroll']
                total_premium += premium

                rates.append({
                    'rate': rate,
                    'final': final,
                    'code': class_code,
                    'premium': premium,
                })

            # Fees
            manual = estimate = total_premium
            estimate += carrier.carrier.expense_constant

            fees = StateModifier.objects.filter(state=state)
            total_fee = 0
            for fee in fees:
                total_fee += (fee.modifier * total_payroll)

            estimate += total_fee

            # Min/max
            max = manual * Decimal(1+(Decimal(state.max_credit)/100))
            min = manual * Decimal(1-(Decimal(state.max_debit)/100))

            carriers.append({
                'carrier': carrier,
                'class_codes': rates,
                'manual': manual,
                'estimate': estimate,
                'fees': fees,
                'max': max,
                'min': min,
                'total_mod': (total_premium * mod) - total_premium,
                'expense_constant': carrier.carrier.expense_constant,
                'terror_fee': total_fee
            })

        request.session['carriers'] = carriers
        request.session['class_codes'] = class_codes
        request.session['form'] = request.POST

        return redirect('home')
