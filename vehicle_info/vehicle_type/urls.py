from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehicle/<int:vehicle_id>', views.vehicle_info_string, name='vehicle'),
    path('vehicle', views.index, name='vehicle_index'),
    path('expected_vehicle', views.index, name='expected_vehicle_index'),
    path('expected_vehicle/<slug:line_number>/<int:vehicle_number>', views.vehicle_expected, name='expected_vehicle'),
    path('expected_vehicle/line/<slug:line_number>/vehicle/<int:vehicle_number>', views.vehicle_expected, name='expected_vehicle'),
]
