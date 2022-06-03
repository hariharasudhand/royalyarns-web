from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from psycopg2 import Date
from .forms import Ry_En_Form, Ry_En_Header
from .models import RY_Enquiry_Header, RY_Enquiry_Items
import subprocess
from django.db.models import Q


def index(request):
    vReg_no = request.GET.get('Rno')
    vFlag = request.POST.get('Rno')
    vStatus = ''
    data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
    data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)

    if vReg_no == None and vFlag == None:
        context = {}
        Unread_Data = RY_Enquiry_Header.objects.filter(Status='0')
        other_status = RY_Enquiry_Header.objects.filter(
            ~Q(Status='0') & ~Q(Status='3'))
        # Ready_For_Quotation = RY_Enquiry_Header.objects.filter(Status='2')
        Req_Yarn_Price = RY_Enquiry_Header.objects.filter(Status='3')

        context['Unread_Data'] = Unread_Data
        context['other_status'] = other_status
        # context['Ready_For_Quotation'] = Ready_For_Quotation
        context['Req_Yarn_Price'] = Req_Yarn_Price

        Count_Unr = len(Unread_Data)
        Count_Upd = len(other_status)
        # Count_Rfq = len(Ready_For_Quotation)
        Count_RYP = len(Req_Yarn_Price)

        context['Count_Unr'] = Count_Unr
        context['Count_Upd'] = Count_Upd
        # context['Count_Rfq'] = Count_Rfq
        context['Count_RYP'] = Count_RYP

        # print(Count_Unr, Count_Upd, Count_Rfq)

        return render(request, 'app/ryn.html', context)

    if vFlag != None:
        data = RY_Enquiry_Items.objects.filter(Reg_no=vFlag)
        data2 = RY_Enquiry_Header.objects.filter(Reg_no=vFlag)
        update_book(request, data, vReg_no, data2)

    form = Ry_En_Form()
    if request.method == 'POST':
        form = Ry_En_Form(request.POST)
        if form.is_valid():
            form.save()
    if len(data2) != 0:
        for item in data2:
            Email_Details = item.Email_Details
            Date = item.Date
            Mill_Rep = item.Mill_Rep
            Marketing_Zone = item.Marketing_Zone
            Mill = item.Mill
            Customer = item.Customer
            if item.Status >= '3':
                vStatus = 'readonly'

    if len(data) != 0:
        for item in data:
            Counts = item.Counts
            Quality = item.Quality
            Type = item.Type
            Blend = item.Blend.replace(" ", "")
            Shade = item.Shade
            Shade_Ref = item.Shade_Ref
            Depth = item.Depth
            UOM = item.UOM
            Quantity = item.Quantity
            Status = item.Status
            Rate = item.Rate
            Amount = item.Amount
            Last_order = item.Last_order

            print("data from database Counts :", Counts)

        context = {
            'Counts': Counts,
            'Quality': Quality,
            'Type': Type,
            'Blend': Blend,
            'Shade': Shade,
            'Shade_Ref': Shade_Ref,
            'Depth': Depth,
            'UOM': UOM,
            'Quantity': Quantity,
            'Status': Status,
            'vReg_no': vReg_no,
            'data': data,
            'data2': data2,
            'Email_Details': Email_Details,
            'Date': Date,
            'Mill_Rep': Mill_Rep,
            'Marketing_Zone': Marketing_Zone,
            'Mill': Mill,
            'Customer': Customer,
            'Feild_Type': vStatus,

        }
    else:
        context = {'Error': 'No data found'
                   }

    return render(request, 'app/ryn2.html', context)


def update_book(request, data, vReg_no, data2):

    visCancel = request.POST.get('txtcancel')

    if len(visCancel) == 0:

        for item in data:
            vid = str(item.id)
            vStatus = '1'
            print("values from form", request.POST.get('Rate'+str(item.id)))
            Rate = request.POST.get('Rate'+str(item.id))
            if Rate != None:
                vStatus = '4'
            RY_Enquiry_Items.objects.filter(id=vid).update(
                Counts=request.POST.get('Counts'+str(item.id)), Quality=request.POST.get('Quality'+str(item.id)), Type=request.POST.get('YarnType'+str(item.id)), Blend=request.POST.get('Blend'+str(item.id)), Shade=request.POST.get('Shade'+str(item.id)), Depth=request.POST.get('Depth'+str(item.id)), UOM=request.POST.get('UOM'+str(item.id)), Quantity=request.POST.get('Quantity'+str(item.id)), Rate=request.POST.get('Rate'+str(item.id)), Amount=request.POST.get('Amount'+str(item.id)), Last_order=request.POST.get('Last_order'+str(item.id)), Status=vStatus)

        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
            Mill=request.POST.get('Mill'), Date=request.POST.get('Date'), Mill_Rep=request.POST.get('Mill_Rep'), Customer=request.POST.get('Customer'), Marketing_Zone=request.POST.get('Marketing_Zone'), Status=vStatus)
    else:

        for item in data:
            vid = str(item.id)
            RY_Enquiry_Items.objects.filter(id=vid).update(Status=2)

        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(Status=2)

    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


def ryn2(request):
    return render(request, 'app/ryn2.html')
