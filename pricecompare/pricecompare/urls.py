from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pricecompare.views import HomeView, QuoteView
from pricecompare.ajax_views import ClassCodeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^(?P<carrier_id>\d+)/$', HomeView.as_view(), name="detail"),
    url(r'quote/$', QuoteView.as_view(), name="quote"),
    url(r'ajax/class_codes/$', ClassCodeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
