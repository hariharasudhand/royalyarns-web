from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ryn2', views.ryn2, name='ryn2'),

]
