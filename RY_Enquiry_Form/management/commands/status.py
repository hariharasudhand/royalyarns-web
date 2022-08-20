from django.core.management import BaseCommand
from RY_Enquiry_Form.models import RY_Enquiry_Items, RY_Enquiry_Header
import sys


mail = "logeshwari.m.k@weeroda.com"

class Command(BaseCommand):
    help = "Status Update"

    def handle(self, *args, **kwargs):
        sts= '14'
        reg= '10'
        RY_Enquiry_Items.objects.filter(Reg_no=reg).update(Status=sts)
        RY_Enquiry_Header.objects.filter(Reg_no=reg).update(Status=sts)
        