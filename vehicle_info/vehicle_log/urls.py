from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('', views.index, name='log_index'),
    path('vehicle', views.vehicle_log, name='vehicle_log'),
    path('vehicle/<str:vehicle_id>', views.vehicle_log, name='vehicle_log'),
    path('vehicle_type/<str:key>', views.vehicle_type, name='vehicle_type'),
    path('lines', views.lines_with_log, name='lines'),
    path('line/<str:line>', views.line_log, name='line_log'),
    path('block_ref/<str:block_ref>', views.block_ref_log, name='block_ref_log'),
    path('operator', views.operator, name='operator'),
    path('operator/<int:prefix>', views.operator, name='operator'),
]
