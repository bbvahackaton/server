
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from inegi.views import InegiView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^get_data_from_inegi/(?P<id_pyme>[0-9]+)$', InegiView.get_data_from_inegi, name='get_data_from_inegi'),
]
