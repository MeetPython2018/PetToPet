from django.urls import path
from . import views

app_name = 'petstate'
urlpatterns = [
    path('write_TW', views.write_TW, name='write_TW'),
    path('intensify', views.intensify, name='intensify'),
    path('intensify_son', views.intensify_son, name='intensify_son'),
]