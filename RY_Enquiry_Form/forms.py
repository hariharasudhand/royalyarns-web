from django.forms import ModelForm
from .models import RY_Enquiry_Header, RY_Enquiry_Items


class Ry_En_Form(ModelForm):
    class Meta:
        model = RY_Enquiry_Items
        fields = '__all__'


class Ry_En_Header(ModelForm):
    class Meta:
        model = RY_Enquiry_Header
        fields = '__all__'
