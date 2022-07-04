from genericpath import exists
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django import http
from psycopg2 import Date
from django.http import HttpResponseRedirect
from .forms import Ry_En_Form, Ry_En_Header, User_Form, Comment_Form
from .models import RY_Enquiry_Header, RY_Enquiry_Items, User_Details, customer_comments
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib import auth
from datetime import datetime


@csrf_exempt
def index(request):
    vReg_no = request.GET.get('Rno')
    vFlag = request.POST.get('Rno')
    vStatus = ''
    data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
    data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)

    data3 = customer_comments.objects.filter(Reg_no=vReg_no)

    # for dt in data3:
    #     print(" reg_no", dt.Reg_no)
    #     print(" comments", dt.Comments)

    #data4 = User_Details.objects.all()

    if vReg_no == None and vFlag == None:
        context = {}
        Unread_Data = RY_Enquiry_Header.objects.filter(Status='0')
        other_status = RY_Enquiry_Header.objects.filter(
            ~Q(Status='0') & ~Q(Status='3'))
        Req_Yarn_Price = RY_Enquiry_Header.objects.filter(Status='3')

        context['Unread_Data'] = Unread_Data
        context['other_status'] = other_status
        context['Req_Yarn_Price'] = Req_Yarn_Price

        Count_Unr = len(Unread_Data)
        Count_Upd = len(other_status)
        Count_RYP = len(Req_Yarn_Price)

        context['Count_Unr'] = Count_Unr
        context['Count_Upd'] = Count_Upd
        context['Count_RYP'] = Count_RYP
        return render(request, 'app/ryn.html', context)

    if vFlag != None:
        print("vFlag", vFlag)
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

        # This is the index for item table records, fix this
        # for item in data:
        #     Counts = item.Counts
        #     Quality = item.Quality
        #     Type = item.Type
        #     Blend = item.Blend.replace(" ", "")
        #     Shade = item.Shade
        #     Shade_Ref = item.Shade_Ref
        #     Depth = item.Depth
        #     UOM = item.UOM
        #     Quantity = item.Quantity
        #     Status = item.Status
        #     Rate = item.Rate
        #     Amount = item.Amount
        #     Last_order = item.Last_order

        # print("data from database Counts :", Counts)
        context = {
            # 'Counts': Counts,
            # 'Quality': Quality,
            # 'Type': Type,
            # 'Blend': Blend,
            # 'Shade': Shade,
            # 'Shade_Ref': Shade_Ref,
            # 'Depth': Depth,
            # 'UOM': UOM,
            # 'Quantity': Quantity,
            # 'Status': Status,
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
            'data3': data3,

        }
    else:
        context = {'Error': 'No data found'
                   }

    return render(request, 'app/ryn2.html', context)


def update_book(request, data, vReg_no, data2):

    visCancel = request.POST.get('txtcancel')

    if len(visCancel) == 0:
        vRowCount = int(request.POST.get('txtRowCount'))
        print("Row Count : ", vRowCount)

        for itemIndex in range(vRowCount):
            vRowIndex = itemIndex+1
            print("Processing Index", vRowIndex)
            DBItemID = request.POST.get('DBID'+str(vRowIndex))
            print("Processing DBItemID", str(DBItemID))
            vStatus = '1'
            #print("values from form", request.POST.get('Counts'+str(vRowIndex)))
            Rate = request.POST.get('Rate'+str(vRowIndex))
            if Rate != None:
                vStatus = '4'

            # if DBItemID is None that means this is a newly added row, as when the page
            # loads db record index will be filled in the hidden field which is queried and
            # stored above in DBItemID field
            if DBItemID != None:
                RY_Enquiry_Items.objects.filter(id=DBItemID, Reg_no=vReg_no).update(
                    Counts=request.POST.get('Counts'+str(vRowIndex)), Quality=request.POST.get('Quality'+str(vRowIndex)), Type=request.POST.get('YarnType'+str(vRowIndex)), Blend=request.POST.get('Blend'+str(vRowIndex)), Shade=request.POST.get('Shade'+str(vRowIndex)), Depth=request.POST.get('Depth'+str(vRowIndex)), UOM=request.POST.get('UOM'+str(vRowIndex)), Quantity=request.POST.get('Quantity'+str(vRowIndex)), Rate=request.POST.get('Rate'+str(vRowIndex)), Amount=request.POST.get('Amount'+str(vRowIndex)), Last_order=request.POST.get('Last_order'+str(vRowIndex)), Status=vStatus)
            else:
                # else insert new value.
                ryNewItem = RY_Enquiry_Items(Reg_no=vReg_no, Counts=request.POST.get('Counts'+str(vRowIndex)), Quality=request.POST.get('Quality'+str(vRowIndex)), Type=request.POST.get('YarnType'+str(vRowIndex)), Blend=request.POST.get('Blend'+str(vRowIndex)), Shade=request.POST.get('Shade'+str(vRowIndex)), Depth=request.POST.get(
                    'Depth'+str(vRowIndex)), UOM=request.POST.get('UOM'+str(vRowIndex)), Quantity=request.POST.get('Quantity'+str(vRowIndex)), Rate=request.POST.get('Rate'+str(vRowIndex)), Amount=request.POST.get('Amount'+str(vRowIndex)), Last_order=request.POST.get('Last_order'+str(vRowIndex)), Status=vStatus)
                ryNewItem.save()

        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
            Mill=request.POST.get('Mill'), Date=request.POST.get('Date'), Mill_Rep=request.POST.get('Mill_Rep'), Customer=request.POST.get('Customer'), Marketing_Zone=request.POST.get('Marketing_Zone'), Status=vStatus)

    elif visCancel == 'comment':
        print("this is inside elseif")
        command_update(request, vReg_no)

    else:
        print("this is inside else")
        for item in data:
            vid = str(item.id)
            RY_Enquiry_Items.objects.filter(id=vid).update(Status=2)

        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(Status=2)

    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


def command_update(request, vReg_no):
    vCommand = request.POST.get('Ccomment')
    vCustomer = request.POST.get('Customer')
    now = datetime.now()
    vDT = now.strftime("%d/%m/%Y:%H:%M:%S")
    print("this is time and date", vDT)
    vRno = vReg_no
    if len(vCommand) != 0:
        customer_comments.objects.create(
            Comments=vCommand, Reg_no=vRno, UserId=vCustomer, DT=vDT)
        # messages.success(request, 'Form successfully submitted')
        return http.HttpResponseRedirect('')

    else:
        return render(request, 'app/ryn2.html')


def ryn2(request):
    return render(request, 'app/ryn2.html')


def register(request):
    return render(request, 'app/register.html')


@csrf_exempt
def validateUser(request):
    vUser = request.POST.get('uname')
    vPassword = request.POST.get('psw')
    vRole = ''
    print(vUser, vPassword, "***********************")
    # add one more filter for password roles:agent,buyer and 3,4 suplier
    # when user role is 0,1,2 agent then only see home page if the status is 5
    vData3 = User_Details.objects.filter(
        UserName=vUser, Password=vPassword)
    for item in vData3:
        vRole = item.Role
    print(vRole, "/*/////////*/*****//////////")
    if vData3.count() != 0:
        print("user is available")
        return render(request=request, template_name="app/ryn.html")
    else:
        print(" user is not available")
        return render(request=request, template_name="app/loginagain.html")
