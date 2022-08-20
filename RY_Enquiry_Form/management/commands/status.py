from django.core.management import BaseCommand
from RY_Enquiry_Form.models import RY_Enquiry_Items, RY_Enquiry_Header
import sys


mail = "logeshwari.m.k@weeroda.com"


class Command(BaseCommand):
    help = "Status Update"

    def add_arguments(self, parser):

        parser.add_argument('reg_no')
        parser.add_argument('sts')

        parser.add_argument("created_by", nargs='?', default=None)

    def handle(self, *args, **options):

        reg_no = options['reg_no']
        sts = options['sts']

        created_by = options['created_by']

        if(created_by != None):
            RY_Enquiry_Items.objects.filter(
                Reg_no=reg_no).update(CreatedByUser=created_by)
            RY_Enquiry_Header.objects.filter(
                Reg_no=reg_no).update(CreatedByUser=created_by)

        RY_Enquiry_Items.objects.filter(Reg_no=reg_no).update(Status=sts)
        RY_Enquiry_Header.objects.filter(Reg_no=reg_no).update(Status=sts)
