from contextlib import nullcontext
from genericpath import exists
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from ast import Store
from dataclasses import dataclass
from django.shortcuts import redirect, render
from django import http
from psycopg2 import Date
from django.http import HttpResponseRedirect
from .forms import Ry_En_Form, Ry_En_Header, User_Form, Comment_Form
from .models import purchase, User_Details
from .DAO import DAO
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib import auth
from datetime import datetime

vDAO = DAO("dao")


# @csrf_exempt
# def checkUserCookie(request):

#     if request.COOKIES.get('role') == None:
#         return render(request, 'app/ryn_login.html')


@csrf_exempt
def index(request):

    vReg_no = None
    vLoggedInRole = request.COOKIES.get('role')
    vStatus = ''

    # #
    # TO:DO - put this inside a reusable method checkLoginStatus
    #
    if vLoggedInRole == None:
        return render(request, 'app/ryn_login.html')

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
        data3 = vDAO.GetComments(vReg_no, vLoggedInRole)

        if request.method == 'POST':

            # data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
            # data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)
            __update_enquiryForm(request, vENQ_Items, vReg_no, vENQ_Header)

            # form = Ry_En_Form()
            # form = Ry_En_Form(request.POST)
            # if form.is_valid():
            #     form.save()

        context = __prepareUIData(
            vReg_no, vENQ_Items, vENQ_Header, data3, vLoggedInRole)
        print("Status of Enq ", context['vStatus'])
        if (context['vStatus'] == '6'):
            return render(request, 'app/quotation.html', context)
        else:
            return render(request, 'app/ryn2.html', context)


def __update_enquiryForm(request, vENQ_Items, vReg_no, vENQ_Header):
    vUserID = request.COOKIES.get('username')
    vMill = request.POST.get('Mill')
    vDate = request.POST.get('Date')
    vMill_Rep = request.POST.get('Mill_Rep')
    vCustomer = request.POST.get('Customer')
    vMarketing_Zone = request.POST.get('Marketing_Zone')
    vUser = request.POST.get('UserName')
    vNow = datetime.now()

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

            # Supplier Entered Rates
            vRate = request.POST.get('Rate'+str(vRowIndex))
            vAmount = request.POST.get('Amount'+str(vRowIndex))
            vLast_order = request.POST.get('Last_order'+str(vRowIndex))

            # Agent ReEntered Rates
            vARate = request.POST.get('Arate'+str(vRowIndex))
            vAAmount = request.POST.get('Aamount'+str(vRowIndex))
            vALast_order = request.POST.get('Alast_order'+str(vRowIndex))

            print("****** Rate", vRate)
            print("****** Amount", vAmount)
            print("****** Last Order", vLast_order)

            print("****** Rate", vARate)
            print("****** Amount", vAAmount)
            print("****** Last Order", vALast_order)

            if vARate != None:
                vStatus = '5'
            elif vRate != None:
                vStatus = '4'

            # if DBItemID is None that means this is a newly added row, as when the page
            # loads db record index will be filled in the hidden field which is queried and
            # stored above in DBItemID field
            if DBItemID != None:
                print("inside updating existing", vStatus)
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount, vLast_order, vStatus, 1,
                                      vARate, vAAmount, vALast_order, vUserID, vNow)

            else:
                # else insert new value.
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount,
                                      vLast_order, vStatus, 0, vARate, vAAmount, vALast_order,
                                      vUserID, vNow)

        vDAO.StoreEnquiryHeader(vReg_no, vMill, vDate,
                                vMill_Rep, vCustomer, vMarketing_Zone, vStatus, vUserID, vNow)

    elif vBtnAction == 'comment':
        print("this is inside elseif")
        __command_update(request, vReg_no)

    elif vBtnAction == 'cancel':
        vDAO.UpdateEnquiryStatus(vReg_no, 2)

    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


def __command_update(request, vReg_no):
    vComments = request.POST.get('Ccomment')
    now = datetime.now()
    vUserID = request.COOKIES.get('username')
    print('this is userName', vUserID)
    vRole = request.COOKIES.get('role')
    vNow = datetime.now()
    vDT = now.strftime("%d/%m/%Y:%H:%M:%S")
    vComments_to = request.POST.get('vComments_to')

    print("this is time and date", vDT)

    if len(vComments) != 0:

        vDAO.StoreComments(vComments, vReg_no, vUserID, vDT, vComments_to)
        # messages.success(request, 'Form successfully submitted')
        return http.HttpResponseRedirect('')

    else:
        return render(request, 'app/ryn2.html')


def ryn2(request):
    # #
    # TO:DO - put this inside a reusable method checkLoginStatus
    #

    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')

    res = User_Details.objesct.get(id=id)
    return render(request, 'app/ryn2.html', {'det': res})


def register(request):
    # #
    # TO:DO - put this inside a reusable method checkLoginStatus
    #
    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')
    return render(request, 'app/register.html')


def confirmpo(request):
    # #
    # TO:DO - put this inside a reusable method checkLoginStatus
    #
    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')

    vReg_no = ''
    vPONumber = ''

    if request.method == 'POST':
        vReg_no = request.POST.get('Rno')
        vPONumber = request.POST.get('txtPONumber')
        vPOPdf = request.FILES['txtPOPDF']

        store = purchase()
        store.pono = vPONumber
        store.popdf = vPOPdf
        store.save()
        print("vReg_no", vReg_no)
        print("vPONumber", vPONumber)

        return render(request, 'app/confirmpo.html')
    else:
        return render(request, 'app/quotations.html')


def __handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def __prepareUIData(vReg_no, vENQ_Items, data2, data3, vRole):

    context = {'Error': 'No data found'}
    Default_Enq_Fileds = ''
    Supplier_Fileds = ''
    Quotation_ready = ''
    vStatus = ''
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
            vStatus = item.Status
            print("status in view :", vStatus)

            if item.Status >= '3':
                Default_Enq_Fileds = 'readonly'
            if item.Status >= '4':
                Supplier_Fileds = 'readonly'
            if item.Status >= '5':
                # Probably there is a better status - i will use this in the Agent ReEntered Field as readonly
                Quotation_ready = 'readonly'

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
            'Quotation_ready': Quotation_ready,
            'vStatus': vStatus,
            'data3': data3,
            'vRole': vRole

        }

    return context

##
#  Authentication Functions
##

# start of login form validation


@csrf_exempt
def checklogin(request):
    # getting the input from the Login from:
    username = None
    password = None

    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

    # Check username and password combines exists in the database,
    # if so fetch the role
    vData3 = vDAO.GetUserInfo(username, password)
    if len(vData3) > 0:

        # request.session['user'] = username
        # request.session['role'] =

        # getting the cookies from the login Page using Context:
        # context = {
        #     'username': username,
        #     'role': vRole,
        # }
        response = redirect('/')
        # setting cookies
        response.set_cookie('username', username)
        response.set_cookie('role', vData3[0].Role)
        return response

    else:
        messages.success(request, "Unvalid User Name or Password!")
        return render(request, 'app/ryn_login.html')


def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    # deleting cookies
    response.delete_cookie('username')
    response.delete_cookie('logged_in')
    response.delete_cookie('role')

    return response


def login(request):
    return render(request, 'app/ryn_login.html')
