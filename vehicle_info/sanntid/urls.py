from django.urls import path

from . import views

app_name = 'sanntid'
urlpatterns = [
    path('', views.select_stop),
    path('stops_latlon', views.stops_latlon, name='stops_latlon'),
    path('stop/<str:stop>', views.stop_departures, name='stop_departures'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('vehicles/<str:line>/<str:line2>', views.vehicle_status, name='vehicles2'),
    path('vehicles/<str:line>', views.vehicle_status, name='vehicles'),
]
