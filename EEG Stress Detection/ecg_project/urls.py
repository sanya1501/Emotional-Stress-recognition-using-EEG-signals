# ecg/urls.py
from django.urls import path
from ecg import views

urlpatterns = [
    path('', views.main, name='home'),
    path('detect/', views.home, name='home'),
    path('history/', views.history, name='history'),
]
