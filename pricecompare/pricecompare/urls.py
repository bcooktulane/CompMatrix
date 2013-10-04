from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pricecompare.views import SearchView, ThankYou, HomeView, ContactView, QuoteView, CompareView, DetailView
from pricecompare.ajax_views import ClassCodeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^contact/$', ContactView.as_view(), name="contact"),
    url(r'^thankyou/$', ThankYou.as_view(), name="thankyou"),
    url(r'^search/$', SearchView.as_view(), name="home"),
    url(r'^(?P<carrier_state_id>\d+)/$', DetailView.as_view(), name="detail"),
    url(r'quote/$', QuoteView.as_view(), name="quote"),
    url(r'compare/$', CompareView.as_view(), name="compare"),
    url(r'ajax/class_codes/$', ClassCodeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
