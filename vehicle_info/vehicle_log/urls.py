from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('', views.index, name='log_index'),
    path('vehicle', views.vehicle_log, name='vehicle_log'),
    path('vehicle/<str:vehicle_id>', views.vehicle_log, name='vehicle_log'),
    path('line/<str:line>', views.line_log, name='line_log'),
    path('block_ref/<str:block_ref>', views.block_ref_log, name='block_ref_log'),
]
