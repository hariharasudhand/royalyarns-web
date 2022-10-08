from unicodedata import name
from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('ryn2', views.ryn2, name='ryn2'),
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
    path('StoreCopNumber', views.StoreCopNumber, name='StoreCopNumber'),
    path('dashboard', views.dashboard, name='dashboard' ),
    path('Upload', views.Upload, name='Upload'),
    path('groupDelete/<int:id>', views.groupDelete, name='groupDelete'),
    path('NewEntry', views.NewEntry, name='NewEntry'),
    path('NewEnquiry', views.NewEnquiry, name= 'NewEnqiury'),
    path('Errors', views.Errors, name='Errors'),
]
 