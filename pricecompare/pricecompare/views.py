from django.views.generic import TemplateView

from pricecompare.models import State, IndustryGroup


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = {
            'states': State.objects.filter(active=True).order_by('name'),
            'industries': IndustryGroup.objects.all()
        }
        return context
