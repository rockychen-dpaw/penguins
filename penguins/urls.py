from __future__ import absolute_import
from django.urls import include,path
from observations.api import API_URLS
from observations.sites import site
from observations.views import HelpPage

urlpatterns = [
    path('api/', include((API_URLS, 'observations'), namespace='api')),
    path('help/', HelpPage.as_view(), name='help_page'),
    path('', site.urls),
]
