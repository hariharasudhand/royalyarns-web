from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('ryn2', views.ryn2, name='ryn2'),
    path('', views.register, name="register"),
    path('login', views.login, name="login"),
    path('checklogin', views.checklogin, name="checklogin"),
    path('logout', views.logout, name="logout"),
    path('confirmpo', views.confirmpo, name='confirmpo'),
    path('UploadExcel', views.UploadExcel, name='UploadExcel'),

]
 