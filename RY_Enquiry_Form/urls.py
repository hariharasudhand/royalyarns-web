from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('ryn2', views.ryn2, name='ryn2'),
    #path('', views.register, name="register"),
    path('login', views.login, name="login"),
    path('checklogin', views.checklogin, name="checklogin"),
    path('logout', views.logout, name="logout"),
    path('confirmpo', views.confirmpo, name='confirmpo'),
    path('UploadExcel', views.UploadExcel, name='UploadExcel'),
    path('quantityCheck', views.quantityCheck, name='quantityCheck'),
    path('register', views.register, name='register'),
    path('activate/<str:id1>', views.activate, name='activate'),
    path('assignrole', views.assignrole, name='assignrole'),
    path('group', views.group, name='group'),
    path('roleassigned', views.roleassigned, name='roleassigned'),
    path('groupassigned', views.groupassigned, name='groupassigned'),
    path('QuantityStore', views.QuantityStore, name='QuantityStore' ),
]
 