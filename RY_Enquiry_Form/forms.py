from django.forms import ModelForm
from .models import RY_Enquiry_Header, RY_Enquiry_Items, User_Details, customer_comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class Ry_En_Form(ModelForm):
    class Meta:
        model = RY_Enquiry_Items
        fields = '__all__'


class Ry_En_Header(ModelForm):
    class Meta:
        model = RY_Enquiry_Header
        fields = '__all__'


class User_Form(ModelForm):
    class Meta:
        model = User_Details
        fields = '__all__'


class Comment_Form(ModelForm):
    class Meta:
        model = customer_comments
        fields = '__all__'
