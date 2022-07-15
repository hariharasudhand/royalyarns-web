from genericpath import exists
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from ast import Store
from dataclasses import dataclass
from django.shortcuts import redirect, render
from django import http
from psycopg2 import Date
from django.http import HttpResponseRedirect
from .forms import Ry_En_Form, Ry_En_Header, User_Form, Comment_Form
# from .models import RY_Enquiry_Header, RY_Enquiry_Items, User_Details, customer_comments
from .DAO import DAO
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib import auth
from datetime import datetime

vDAO = DAO("dao")


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
        context = vDAO.GetLandingPageData()
        #print("**********>> context", context)
        return render(request, 'app/ryn.html', context)
    else:
        ##
        # Fetch Header Values & Item Values for the supplied RegNo (Registation Number)
        ##
        vENQ_Items = vDAO.GetEnquiryItems(vReg_no)
        vENQ_Header = vDAO.GetEnquiryHeader(vReg_no)

        ##
        # Fetch Comments associated with the RegNo (Registation Number)
        ##
        data3 = vDAO.GetComments(vReg_no)

        if request.method == 'POST':

            # data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
            # data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)
            __update_enquiryForm(request, vENQ_Items, vReg_no, vENQ_Header)

            # form = Ry_En_Form()
            # form = Ry_En_Form(request.POST)
            # if form.is_valid():
            #     form.save()

        context = __prepareUIData(vReg_no, vENQ_Items, vENQ_Header, data3)
        return render(request, 'app/ryn2.html', context)


def __update_enquiryForm(request, vENQ_Items, vReg_no, vENQ_Header):

    vMill = request.POST.get('Mill')
    vDate = request.POST.get('Date')
    vMill_Rep = request.POST.get('Mill_Rep')
    vCustomer = request.POST.get('Customer')
    vMarketing_Zone = request.POST.get('Marketing_Zone')

    ##
    # *** vBtnAction field points to hBtnAction hidden field in the form
    # *** if hBtnAction is sap , this means Button "Save And Proceed " has been clicked
    # *** if hBtnAction is cancel , this means Button "Proceed " has been clicked
    # *** if hBtnAction is comment , this means Button "Comment Add " has been clicked
    #

    vBtnAction = request.POST.get('hBtnAction')
    #print("***** vBtnAction", vBtnAction)
    vStatus = 0

    if vBtnAction == 'sap':

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

            vCounts = request.POST.get('Counts'+str(vRowIndex))

            vQuality = request.POST.get('Quality'+str(vRowIndex))
            vYarnType = request.POST.get('YarnType'+str(vRowIndex))
            vBlend = request.POST.get('Blend'+str(vRowIndex))
            vShade = request.POST.get('Shade'+str(vRowIndex))
            vDepth = request.POST.get('Depth'+str(vRowIndex))
            vUOM = request.POST.get('UOM'+str(vRowIndex))
            vQuantity = request.POST.get('Quantity'+str(vRowIndex))

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
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount, vLast_order, vStatus, 1)

            else:
                # else insert new value.
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount, vLast_order, vStatus, 0)

        vDAO.StoreEnquiryHeader(vReg_no, vMill, vDate,
                                vMill_Rep, vCustomer, vMarketing_Zone, vStatus)

    elif vBtnAction == 'comment':
        print("this is inside elseif")
        __command_update(request, vReg_no)

    elif vBtnAction == 'cancel':
        vDAO.UpdateEnquiryStatus(vReg_no, 2)

    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


def __command_update(request, vReg_no):
    vCommand = request.POST.get('Ccomment')
    vCustomer = request.POST.get('Customer')
    now = datetime.now()
    vDT = now.strftime("%d/%m/%Y:%H:%M:%S")
    print("this is time and date", vDT)

    if len(vCommand) != 0:

        vDAO.StoreComments(vCommand, vReg_no, vCustomer, vDT)
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
    # print(vUser, vPassword, "***********************")
    # add one more filter for password roles:agent,buyer and 3,4 suplier
    # when user role is 0,1,2 agent then only see home page if the status is 5
    vData3 = vDAO.GetUserInfo(vUser, vPassword)
    for item in vData3:
        vRole = item.Role
    print(vRole, "/*/////////*/*****//////////")
    if vData3.count() != 0:
        print("user is available")
        return render(request=request, template_name="app/ryn.html")
    else:
        print(" user is not available")
        return render(request=request, template_name="app/loginagain.html")


# def storedata(request):
#     if request.method == 'POST':
#         a = request.POST["Counts"]
#         b = request.POST["Quality"]
#         c = request.POST["YarnType"]
#         d = request.POST["Blend"]
#         e = request.POST["Shade"]
#         f = request.POST["Depth"]
#         g = request.POST["UOM"]
#         h = request.POST["Quantity"]

#         store = RY_Enquiry_Items()
#         store.Counts = a
#         store.Quality = b
#         store.Type = c
#         store.Blend = d
#         store.Shade = e
#         store.Depth = f
#         store.UOM = g
#         store.Quantity = h
#         store.save()

#         return render(request, 'app/ryn2.html')


def __prepareUIData(vReg_no, vENQ_Items, data2, data3):

    context = {'Error': 'No data found'}
    Default_Enq_Fileds = ''
    Supplier_Fileds = ''
    vFieldStatus = ''
    if len(data2) != 0:
        for item in data2:
            Email_Details = item.Email_Details
            Date = item.Date
            Mill_Rep = item.Mill_Rep
            Marketing_Zone = item.Marketing_Zone
            Mill = item.Mill
            Customer = item.Customer
            # Item Status >= 3 is for Supplier to enter Rates
            Supplier_Fileds = ''
            if item.Status >= '3':
                Default_Enq_Fileds = 'readonly'
            if item.Status >= '4':
                Supplier_Fileds = 'readonly'

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
            'Default_Enq_Fileds': Default_Enq_Fileds,
            'Supplier_Fileds': Supplier_Fileds,
            'data3': data3,

        }

    return context
