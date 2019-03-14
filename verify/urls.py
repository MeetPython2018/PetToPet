from django.urls import path
from . import views
app_name = 'verify'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('wel/', views.wel, name='wel'),
    path('register/', views.register, name='register'),
    path('secede/', views.secede, name='secede')
]