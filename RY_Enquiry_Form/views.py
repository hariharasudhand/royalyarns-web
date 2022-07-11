from genericpath import exists
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from ast import Store
from asyncio.windows_events import NULL
from dataclasses import dataclass
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

    vReg_no = None
    vStatus = ''

    ##
    #  Rno (Registation Number) is passed as Query String as
    #  (GET)
    #   or
    #  (POST)
    ##
    if request.method == 'POST':
        vReg_no = request.POST.get('Rno')
    else:
        vReg_no = request.GET.get('Rno')

    print("******* vRegNo", vReg_no)
    ##
    #  When the home page is accessed , all enquiries are to be displayed
    #  Rno will be empty not available in GET or POST varibale vReg_no will be empty
    ##
    if vReg_no == None:
        context = GetLandingPageData(request)
        #print("**********>> context", context)
        return render(request, 'app/ryn.html', context)
    else:
        ##
        # Fetch Header Values & Item Values for the supplied RegNo (Registation Number)
        ##
        vENQ_Items = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
        vENQ_Header = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)

        ##
        # Fetch Comments associated with the RegNo (Registation Number)
        ##
        data3 = customer_comments.objects.filter(Reg_no=vReg_no)

        if request.method == 'POST':

            # data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
            # data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)
            update_book(request, vENQ_Items, vReg_no, vENQ_Header)

            # form = Ry_En_Form()
            # form = Ry_En_Form(request.POST)
            # if form.is_valid():
            #     form.save()

        context = prepareUIData(vReg_no, vENQ_Items, vENQ_Header, data3)
        return render(request, 'app/ryn2.html', context)


def update_book(request, vENQ_Items, vReg_no, vENQ_Header):

    visCancel = request.POST.get('txtcancel')
    #print("***** visCancel", visCancel)
    vStatus = 0
    if len(visCancel) == 0:
        print("***** txtRowCount", request.POST.get('txtRowCount'))
        vRowCount = 0
        if (request.POST.get('txtRowCount') != None):
            vRowCount = int(request.POST.get('txtRowCount'))
            print("Row Count : ", vRowCount)

        for itemIndex in range(vRowCount):
            vRowIndex = itemIndex+1
            print("Processing Index", vRowIndex)
            DBItemID = request.POST.get('DBID'+str(vRowIndex))
            print("Processing DBItemID", str(DBItemID))
            vStatus = '1'

            vRate = request.POST.get('Rate'+str(vRowIndex))
            vAmount = request.POST.get('Amount'+str(vRowIndex))
            vLast_order = request.POST.get('Last_order'+str(vRowIndex))
            print("****** Rate", vRate)
            print("****** Amount", vAmount)
            print("****** Last Order", vLast_order)

            if vRate != None:
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
        for item in vENQ_Items:
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

def storedata(request):
        if request.method == 'POST':
            a=request.POST["Counts"]
            b=request.POST["Quality"]
            c=request.POST["YarnType"]
            d=request.POST["Blend"]
            e=request.POST["Shade"]
            f=request.POST["Depth"]
            g=request.POST["UOM"]
            h=request.POST["Quantity"]
            
            store=RY_Enquiry_Items()
            store.Counts=a
            store.Quality=b
            store.Type=c
            store.Blend=d
            store.Shade=e
            store.Depth=f
            store.UOM=g
            store.Quantity=h
            store.save()
            
            return render(request , 'app/ryn2.html')



def prepareUIData(vReg_no, vENQ_Items, data2, data3):

    context = {'Error': 'No data found'}
    vFieldStatus = ''
    if len(data2) != 0:
        for item in data2:
            Email_Details = item.Email_Details
            Date = item.Date
            Mill_Rep = item.Mill_Rep
            Marketing_Zone = item.Marketing_Zone
            Mill = item.Mill
            Customer = item.Customer
            if item.Status >= '3':
                vFieldStatus = 'readonly'

    if len(vENQ_Items) != 0:

        context = {
            'vReg_no': vReg_no,
            'data': vENQ_Items,
            'data2': data2,
            'Email_Details': Email_Details,
            'Date': Date,
            'Mill_Rep': Mill_Rep,
            'Marketing_Zone': Marketing_Zone,
            'Mill': Mill,
            'Customer': Customer,
            'Feild_Type': vFieldStatus,
            'data3': data3,

        }

    return context


def GetLandingPageData(request):

    #context = {'Error': 'No data found'}
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

    return context