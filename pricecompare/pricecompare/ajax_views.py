from django import http
from django.utils import simplejson as json
from django.views.generic import View

from pricecompare.models import State, IndustryGroup, LossCost


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class ClassCodeView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        #industry = request.GET.get('industry')
        q = request.GET.get('q', None)

        try:
            state = State.objects.get(abbreviation=state)
            #industry = IndustryGroup.objects.get(pk=industry)
        except State.DoesNotExist:
            pass
        #except IndustryGroup.DoesNotExist:
        #    pass

        lc = LossCost.objects.filter(state=state)
                                     #class_code__industry_group=industry)

        if q:
            lc = lc.filter(class_code__name__icontains=q)

        codes = []
        for l in lc:
            codes.append({
                'code': l.class_code.code,
                'name': l.class_code.name,
            })

        return self.render_to_response({'codes':codes})
