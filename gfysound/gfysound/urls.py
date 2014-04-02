from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import SubmissionCreateView, make_it


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name='main.html')),
    #url(r'^$', SubmissionCreateView.as_view()),
    url(r'^$', make_it, name='home'),
    url(r'^submit/$', make_it, name='make_it'),
    url(r'^(?P<v>[a-zA-Z0-9_-]{11})/(?P<g>[a-zA-Z]\w+)', make_it, name='make_it2'),
    url(r'^(?P<v>[a-zA-Z0-9_-]{11})$', SubmissionCreateView.as_view()),

    # Examples:
    # url(r'^$', 'gfysound.views.home', name='home'),
    # url(r'^gfysound/', include('gfysound.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
