from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pricecompare.views import *
from pricecompare.ajax_views import ClassCodeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'ajax/class_codes/$', ClassCodeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
