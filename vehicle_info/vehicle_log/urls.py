from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('vehicle/<str:vehicle_id>', views.vehicle_log, name='vehicle_log'),
    path('line/<str:line>', views.line_log, name='vehicles_on_line'),
]
