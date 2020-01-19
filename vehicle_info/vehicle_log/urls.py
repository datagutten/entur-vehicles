from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('vehicle/<str:vehicle>', views.show_log, name='vehicle_log'),
    path('line/<str:line>', views.vehicles_on_line, name='vehicles_on_line'),
]
