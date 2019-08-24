from django.urls import path

from . import views

urlpatterns = [path('vehicle/<str:vehicle>', views.show_log)
               ]
