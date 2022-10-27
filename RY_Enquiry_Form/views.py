from contextlib import nullcontext
# from crypt import methods
from genericpath import exists
from multiprocessing import context
import re
from unicodedata import name
from urllib import request
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from ast import Return, Store
from dataclasses import dataclass
from django.shortcuts import redirect, render
from django import http
from psycopg2 import Date
from django.http import HttpResponseRedirect
from .forms import Ry_En_Form, Ry_En_Header, User_Form, Comment_Form
from .models import User_Details, Upload_Data, RY_Enquiry_Header, Email_Distribution_Groups
from .DAO import DAO
from .DispatchDAO import DispatchDAO
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib import auth
from datetime import datetime
from .EmailUtil import EMAIL_UTIL
#from .ExcelUtlis import ExcelUtlis
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re
from django.db.models import Q, Count
from .models import RY_Enquiry_Header, RY_Enquiry_Items


vDAO = DAO("dao")
vDispatchDAO = DispatchDAO("DispatchDAO")

@csrf_exempt
def index(request):

    vReg_no = None
    vLoggedInRole = request.COOKIES.get('role')
    vLoggedInUserID = request.COOKIES.get('username')
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

    ##
    #  When the home page is accessed , all enquiries are to be displayed
    #  Rno will be empty not available in GET or POST varibale vReg_no will be empty
    ##
    if vReg_no == None:
        context = vDAO.GetLandingPageData(vLoggedInUserID, vLoggedInRole)
        role = request.COOKIES.get('role')
        return render(request, 'app/ryn.html', context)
    else:
        #CONDITION CHECK FOR NOT TO ACCESS THE DATA THROUGH URL
        #TO CHECK WHEATHER LOGIN USER IS ASSOCIATED WITH THE GROUP HAS THE AUTHORITY TO VIEW THE DATA
        if vLoggedInRole == 'supplier':

            vIs_Auth = vDAO.ToCheck_Supplier(vLoggedInUserID)
            if len(vIs_Auth)==0:
                return HttpResponse('Unauthorised Access')
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
            __update_enquiryForm(request, vENQ_Items, vReg_no, vENQ_Header)


        context = __prepareUIData(
            vReg_no, vENQ_Items, vENQ_Header, data3, vLoggedInRole, vLoggedInUserID)
        
        #If Buyer login quotation form in status 6
        print("context",context['vStatus'])
        if (context['vStatus'] == 6):

            return render(request, 'app/quotation.html', context)
        
        #In status 7 entry form for quantity and quality 
        if (context['vStatus'] == 7):
            res1 = request.COOKIES.get('username')
            vLoggedInRole = request.COOKIES.get('role')
            vItems = vDAO.GetEnquiryItems(vReg_no)
            vHeader = vDAO.GetEnquiryHeader(vReg_no)
            return render(request, 'app/ryn_quantity.html', {'vReg_no':vReg_no, 'user':res1, 'Role':vLoggedInRole, 'Items':vItems, 'Header':vHeader})
        
        # #
        # ##Owner Aprovel
        # #
        # if (context['vStatus'] == 9):
        #     res = RY_Enquiry_Header.objects.filter(Status = 9).exclude()
        #     res1 = request.COOKIES.get('username')
        #     vLoggedInRole = request.COOKIES.get('role')
        #     return render(request, 'app/ryn_Approved.html', {'vReg_no':res, 'user':res1, 'Role':vLoggedInRole})
        
        #
        ##Agent Copnumber Enter form
        #
        if (context['vStatus'] == 12):
            res = RY_Enquiry_Header.objects.get(Reg_no=vReg_no)
            res1 = request.COOKIES.get('username')
            vLoggedInRole = request.COOKIES.get('role')
            return render(request, 'app/Copnumber.html', {'vReg_no':res, 'user':res1, 'Role':vLoggedInRole})
        
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
    vGrpAssignedTo = request.POST.get('vGrp_to')
    vDelivery_Date = request.POST.get('Delivery_Date')
    vReadyStock = request.POST.get('ReadyStock')
    vRateFixed  = request.POST.get('RateFixed')
    
    

    

    ##
    # *** vBtnAction field points to hBtnAction hidden field in the form
    # *** if hBtnAction is sap , this means Button "Save And Proceed " has been clicked
    # *** if hBtnAction is cancel , this means Button "Proceed " has been clicked
    # *** if hBtnAction is comment , this means Button "Comment Add " has been clicked
    #

    vBtnAction = request.POST.get('hBtnAction')
    vStatus = 0
    
    if vBtnAction == 'sap':
        vApprovedRate = request.POST.get('ApprovedRate')
        vRateFixed = request.POST.get('RateFixed')
        vRowCount = 0
        if (request.POST.get('txtRowCount') != None):
            vRowCount = int(request.POST.get('txtRowCount'))
            
        for itemIndex in range(vRowCount):
            vRowIndex = itemIndex+1
            DBItemID = request.POST.get('DBID'+str(vRowIndex))
            if vRateFixed == 'RateFixed':
                vStatus = 4
            else:
                vStatus = 1

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

            # emailComp = EMAIL_UTIL()
            # if vStatus == '3' :
            #     print("this is checking for the mail")
            #     emailComp.send_group('agent-only', '[Terata.io] Comment from User : ' +
            #                  vUserID.split('@')[0]+" /  "+vReg_no, 'test mail for status 3 to 4')
            if vARate != None:
                 vStatus = '4'
                 if vApprovedRate == 'Approved':
                    vStatus = '5'
            elif vRate != None:
                 vStatus = '4'

            # if DBItemID is None that means this is a newly added row, as when the page
            # loads db record index will be filled in the hidden field which is queried and
            # stored above in DBItemID field

            if DBItemID != None:
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount, vLast_order, vStatus, 1,
                                      vARate, vAAmount, vALast_order, vUserID, vNow)
                print("Email tetsting for outside",vStatus)
                if (vStatus == '3') or (vStatus == '4'):
                    print("Email tetsting",vStatus)
                    emailComp = EMAIL_UTIL()
                    emailComp.send_group('agent-only', '[Terata.io] Comment from User : ' +
                                vUserID.split('@')[0]+" /  "+vReg_no,'Price Updated by Mill So Kindly Update your price!'+\
                                '\nhttp://qa.royalyarns.terata.io:7000/?Rno='+vReg_no)
            else:
                # else insert new value.
                vDAO.StoreEnquiryItem(DBItemID, vReg_no, vCounts, vQuality, vYarnType, vBlend,
                                      vShade, vDepth, vUOM, vQuantity, vRate, vAmount,
                                      vLast_order, vStatus, 0, vARate, vAAmount, vALast_order,
                                      vUserID, vNow)
        
        vDAO.StoreEnquiryHeader(vReg_no, vMill, vDate,
                                vMill_Rep, vCustomer, vMarketing_Zone, vStatus, vUserID, vNow,vGrpAssignedTo, vReadyStock, vDelivery_Date)

        
        
    elif vBtnAction == 'comment':
        __command_update(request, vReg_no)

    elif vBtnAction == 'cancel':
        vDAO.UpdateEnquiryStatus(vReg_no, 2,vGrpAssignedTo)

    # elif vBtnAction == 'confirm':
    #     vRegno = request.POST.get("select")
    #     print(vRegno)

    
    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


def __command_update(request, vReg_no):
    vComments = request.POST.get('Ccomment')
    now = datetime.now()
    vUserID = request.COOKIES.get('username')
    vRole = request.COOKIES.get('role')
    vNow = datetime.now()
    vDT = now.strftime("%d/%m/%Y:%H:%M:%S")
    vComments_to = request.POST.get('GroupName')
    supplier_grp = list(Email_Distribution_Groups.objects.values_list('GroupName'))
    grp=[]
    for i in supplier_grp:
        grp.append(i[0])

    if len(vComments) != 0:

        vDAO.StoreComments(vComments, vReg_no, vUserID, vDT, vComments_to)
        # messages.success(request, 'Form successfully submitted')
        html_content = render_to_string(
            "app/emailmessage.html", {'vUserID': vUserID, 'vReg_no': vReg_no})
        text_content = strip_tags(html_content)
        emailComp = EMAIL_UTIL()
        if vComments_to in grp:
            emailComp.send_group(vComments_to, '[Terata.io] Comment from User : ' +
                             vUserID.split('@')[0]+" /  "+vReg_no, html_content)
        elif vComments_to == 'agent':
            emailComp.send_group('agent-only', '[Terata.io] Comment from User : ' +
                             vUserID.split('@')[0]+" /  "+vReg_no, html_content)
        
        elif vComments_to == 'supplier_to_agent':
            emailComp.send_group('agent-only', '[Terata.io] Comment from User : ' +
                             vUserID.split('@')[0]+" /  "+vReg_no, html_content)
        elif vComments_to == 'buyer_to_agent':
            emailComp.send_group('agent-only', '[Terata.io] Comment from User : ' +
                             vUserID.split('@')[0]+" /  "+vReg_no, html_content)
        else:
             emailComp.send_single(vComments_to, '[Terata.io] Comment from User : ' +
                             vUserID.split('@')[0]+" /  "+vReg_no, html_content)
        

        return http.HttpResponseRedirect('')

    else:
        return render(request, 'app/ryn2.html')


def ryn2(request):
    # #
    # TO:DO - put this inside a reusable method checkLoginStatus
    #

    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')

    res = User_Details.objects.get(id=id)
    return render(request, 'app/ryn2.html', {'det': res})

def confirmpo(request):
    ##
    # TO:DO - put this inside a reusable method checkLoginStatus
    #

    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')

    if request.method == 'POST':
        vReg_no = request.POST.get('Rno')
        vPONumber = request.POST.get('txtPONumber')
        list = []  # myfile is the key of a multi value dictionary, values are the uploaded files
        file = request.FILES.getlist('txtPOPDF')
        # myfile is the name of your html file button
        for f in request.FILES.getlist('txtPOPDF'):
            vFiles = RY_Enquiry_Header.objects.get(Reg_no=vReg_no)
            vFiles.Po_PDF = f
            vFiles.save()
            #RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update( Po_PDF=f)
            filename = f.name
            list.append(filename)
       

        vPO_Date = datetime.now()
        vRev_date = datetime.now()

        vDAO.UpdateEnquiryHeader(vReg_no, vPONumber, list, vPO_Date, vRev_date)
        emailComp = EMAIL_UTIL()
        emailComp.send_po('[Terata.io] Please check the PO Number: ', 'po.no'+vPONumber, file)
        print("email was send successfully")

        return HttpResponseRedirect("/")


def __handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def __prepareUIData(vReg_no, vENQ_Items, data2, data3, vLoggedInRole, vLoggedInUserID):

    context = {'Error': 'No data found'}
    Default_Enq_Fileds = ''
    Supplier_Fileds = ''
    Quotation_ready = ''
    vStatus = ''
    Default_Role_Base = ''
    vFieldStatus = ''

    if len(vENQ_Items) != 0:
        for items in vENQ_Items:
            vShade_Ref = items.Shade_Ref
            vAgentRate = items.Agent_Rate
            print(vShade_Ref)

    if len(data2) != 0:
        for item in data2:

            Email_Details = item.Email_Details
            Date = item.Date
            Mill_Rep = item.Mill_Rep
            Marketing_Zone = item.Marketing_Zone
            Mill = item.Mill
            Customer = item.Customer
            vCreatedByUser = item.CreatedByUser
            GrpAssignedTo = item.GrpAssignedTo
            vQuotation_Number = item.Quotation_Number
            vQuotation_Date = item.Quotation_Date
            vDelivery_Date = item.Delivery_Date
            vReadyStock = item.Ready_stock
            vStatus = int(item.Status)
            
            vUserAction = vDAO.GetUserActionByRole(vLoggedInRole, vStatus)
            if len(vUserAction) <= 0:
                context = {'Error': 'User: ' + vLoggedInUserID +
                           'Is Not Authorized to View Record Number :' + vReg_no, 'vStatus': vStatus}
                return context
            elif (vUserAction[0].Action == 'R') and (vUserAction[0].Role == 'agent'):
                Default_Enq_Fileds = 'readonly'
            elif (vUserAction[0].Action == 'W') and (vUserAction[0].Role == 'supplier'):
                Supplier_Fileds = ''
                Default_Enq_Fileds = 'readonly'
            elif (vUserAction[0].Action == 'R') and (vUserAction[0].Role == 'supplier') and (vStatus == 4):
                Supplier_Fileds = ''
                Quotation_ready = ''
                Default_Enq_Fileds = 'readonly'
            elif (vUserAction[0].Action == 'W') and (vUserAction[0].Role == 'agent') and (vStatus >= 4):
                Default_Enq_Fileds = 'readonly'
            elif (vUserAction[0].Role == 'buyer'):
                Default_Enq_Fileds = 'readonly'
            elif (vUserAction[0].Action == 'R') and (vUserAction[0].Role == 'buyer') and (vStatus == 4) : 
                  Default_Enq_Fileds = 'readonly'
                  Quotation_ready = 'readonly'
                    
            else:
                Default_Enq_Fileds = ''
            if vStatus >= 4:

                Supplier_Fileds = 'readonly'
    
    # vMill = RY_Enquiry_Header.objects.filter(Mill=Mill)
    # for items in vMill:
    #     hReg_no = items.Reg_no
    #     print("Reg number for the header table:", hReg_no)
    
    vHShade_ref = RY_Enquiry_Items.objects.filter(Shade_Ref=vShade_Ref).exclude(Agent_Rate = None).last()


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
            'Default_Role_Base': Default_Role_Base,
            'vStatus': vStatus,
            'data3': data3,
            'vLoggedInRole': vLoggedInRole,
            'user': vLoggedInUserID,
            'CreatedByUser':vCreatedByUser,
            'GrpAssignedTo':GrpAssignedTo,
            'vQuotation_Number':vQuotation_Number,
            'vQuotation_Date':vQuotation_Date,
            'vDelivery_Date' :vDelivery_Date,
            'vReadyStock' : vReadyStock,
            'vHShade_ref' : vHShade_ref,
            'supplierGroupNames': vDAO.GetSupplierGroupNames()
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
        if (vData3[0].Role == 'admin'):
            response = redirect('/group')
        # elif (vData3[0].Role == 'buyer'):
        #     response = redirect('/buyer')
        else:
            response = redirect('/')
        # setting cookies
        response.set_cookie('username', username)
        response.set_cookie('role', vData3[0].Role)
        return response

    else:
        messages.success(request, "Invalid User Name or Password! or Not been Permitted")
        return render(request, 'app/ryn_login.html')

# def buyer(request):
#     vLoggedInRole = request.COOKIES.get('role')
#     vLoggedInUserID = request.COOKIES.get('username')
#     context = vDAO.GetLandingPageData(vLoggedInUserID, vLoggedInRole)
#     return render(request, 'app/ryn1.html', context)  

def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    # deleting cookies
    response.delete_cookie('username')
    response.delete_cookie('logged_in')
    response.delete_cookie('role')

    return response


def register(request):
    if request.method == "POST":
        vUserMail = request.POST.get("Uname")
        vPassword = request.POST.get("Password")
        vCPassword = request.POST.get("CPassword")

    if User_Details.objects.filter(UserName=vUserMail).exists():
        messages.info(request, 'email address already exists')
        return render(request, 'app/ryn_login.html')

    if vPassword == vCPassword:

        vDAO.StoreUserDetails(vUserMail, vCPassword)
        emailComp = EMAIL_UTIL()
        emailComp.send_activation_code(vUserMail)

        return HttpResponse('Please confirm your email address to complete the registration')

    else:
        messages.success(request, "Password are not same")
        return render(request, 'app/ryn_login.html')


def login(request):
    return render(request, 'app/ryn_login.html')


def UploadExcel(request):
    if request.method == "POST":
        vUpload = request.FILES['upload']
        vDate = datetime.now()
        vUser = request.COOKIES.get('username')
        vDispatchDAO.StoreUpload_Data(vUpload, vDate, vUser)
    return HttpResponseRedirect('/Upload')


def quantityCheck(request):
    if request.COOKIES.get('role') == None:
        return render(request, 'app/ryn_login.html')
    else:
        return render(request, 'app/ryn_quantity.html')


def activate(request, id1):
    msg = vDAO.ActivateUserDetails(id1)
    if msg == True:
        messages.info(request, 'your profile is under verification')
        return render(request, 'app/ryn_login.html')
    else:
        return HttpResponse('Invalid Activation')


def assignrole(request):
    context = User_Details.objects.filter(Role=None)
    context1 = Email_Distribution_Groups.objects.all()
    User = request.COOKIES.get('username')
    return render(request, 'app/addrole.html', {'context': context, 'context1': context1, 'user':User})


def group(request):
    User = request.COOKIES.get('username')
    context1 = Email_Distribution_Groups.objects.all()
    return render(request, 'app/group.html', {'context1': context1, 'user':User})


def roleassigned(request):
    if request.method == "POST":
        vUSER = request.POST.get("UserName")
        vROLE = request.POST.get("Role")
        vGRP = request.POST.get("GroupName")
        context = User_Details.objects.get(UserName=vUSER)
        context.Role = vROLE
        context.save()

        context1 = Email_Distribution_Groups.objects.get(GroupName=vGRP)
        old = context1.GroupUsersID
        new = str(context.id)
        if old is None:
            context1.GroupUsersID = new+','
        else:
            context1.GroupUsersID = old+','+new+','
        context1.save()

        return HttpResponseRedirect('/assignrole')


def groupassigned(request):
    if request.method == "POST":
        vGRP = request.POST.get("GroupName")
        Email_Distribution_Groups.objects.create(GroupName=vGRP, Status=True)

        return HttpResponseRedirect('/group')


def QuantityStore(request):
    if request.method == "POST":
        vDelivery = request.POST.get("Delivery")
        vPayment = request.POST.get("Payment")
        vPrice = request.POST.get("Price")
        vMatching = request.POST.get("Matching")
        vBuyer = request.POST.get("Buyer")
        vOtherSpecification = request.POST.get("OtherSpecification")
        vSpecification = request.POST.get("Specification")
        vCommision = request.POST.get("Commision")
        vApprovel = request.POST.get("Approvel")
        vRequired = request.POST.get("Required")
        vQuantity_type = request.POST.get("Quantity_type")
        vCommit_date = request.POST.get("Commit_date")
        vFeeder = request.POST.get("Feeder")
        vJacaquard = request.POST.get("Jacaquard")
        vMini_jaq = request.POST.get("Mini_jaq")
        vAuto_stripes = request.POST.get("Auto_stripes")
        vSingle_jersey = request.POST.get("Single_jersey")
        vP_K = request.POST.get("P_K")
        vInterlock = request.POST.get("Interlock")
        vRib = request.POST.get("Rib")
        vWhite = request.POST.get("White")
        vLight = request.POST.get("Light")
        vMedium = request.POST.get("Medium")
        vDark = request.POST.get("Dark")
        vOverdyed = request.POST.get("Overdyed")
        vWhite1 = request.POST.get("White1")
        vLight1 = request.POST.get("Light1")
        vDark1 = request.POST.get("Dark1")
        vPayMode = request.POST.get("PayMode")
        vRupees = request.POST.get("Rupees")
        vNumbers1 = request.POST.get("Numbers1")
        vDate = request.POST.get("Date")
        vBank = request.POST.get("Bank")
        vReg_no = request.POST.get('Rno')
        vDAO.StoreQuantity(vDelivery, vPayment, vPrice, vMatching, vBuyer, vOtherSpecification, vSpecification,
                           vCommision, vApprovel, vRequired, vQuantity_type, vCommit_date, vFeeder, vJacaquard, vMini_jaq, vAuto_stripes, vSingle_jersey, vP_K, vInterlock,
                           vRib, vWhite, vLight, vMedium, vDark, vOverdyed, vWhite1, vLight1, vDark1, vPayMode, vRupees, vNumbers1, vDate, vBank,vReg_no)
        return HttpResponseRedirect('/')


def StoreCopNumber(request):
   
    if request.method == 'POST':
        vCopNumber = request.POST.get("COPNumber")
        vReg_no = request.POST.get("Rno")
        vDAO.StoreCopNumber(vReg_no,vCopNumber)
        return HttpResponseRedirect('/')

def dashboard(request):
    vLoggedInRole = request.COOKIES.get('role')
    completed = RY_Enquiry_Header.objects.filter(Status__exact='14').count()
    inprocess = RY_Enquiry_Header.objects.filter(Q(Status__exact='1') | Q(Status__exact='2') | Q(Status__exact='5') | Q(Status__exact='7') | Q(
        Status__exact='8') | Q(Status__exact='9')| Q(Status__exact='0') | Q(Status__exact='10') | Q(Status__exact='11') | Q(Status__exact='13') | Q(Status__exact='4') | Q(Status__exact='6')| Q(Status__exact='12')| Q(Status__exact='3')).count()
    rejected = RY_Enquiry_Header.objects.filter(
        Status__exact='-1').count()
    count = RY_Enquiry_Header.objects.all().count()

# arrays for monthly graph
    totaleq = []
    mon_0 = []
    mon_in = []
    mon_ex = []
    mon_com = []
    rej = []

    # PSQL Queries done with regex-suffix/prefix
    # total enquires
    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(
            Date__contains=res).count()
        totaleq.append(jan_counts)

    # enquires status for 0 ---- New Enquiry
    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(
            Status='0', Date__contains=res).count()
        mon_0.append(jan_counts)

    # enquires status for 1,2,5,7,8,9,1,0,1,1,1,3,4  --- Internal Review

    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(Q(Status__exact='1') | Q(Status__exact='2') | Q(Status__exact='5') | Q(Status__exact='7') | Q(Status__exact='8') | Q(
            Status__exact='9') | Q(Status__exact='10') | Q(Status__exact='11') | Q(Status__exact='13') | Q(Status__exact='4')).filter(Date__contains=res).count()
        mon_in.append(jan_counts)


    # enquires status for 3,6,12 ---- External

    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(Q(Status__exact='6') | Q(
            Status__exact='12') | Q(Status__exact='3')).filter(Date__contains=res).count()
        mon_ex.append(jan_counts)


    # enquires status for 14 ---- Completed

    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(
            Status='14', Date__contains=res).count()
        mon_com.append(jan_counts)

        #  enquires status for -1 ---- Rejected

    for a in range(0, 12):
        date = '2022-01'
        res = re.sub(r'[0-9]+$',
                    lambda x: f"{str(int(x.group())+a).zfill(len(x.group()))}",
                    date)
        jan_counts = RY_Enquiry_Header.objects.filter(
            Status='-1', Date__contains=res).count()
        rej.append(jan_counts)

    # array for quarterly graph
    qt_total = []
    qt_0 = []
    qt_in = []
    qt_ex= []
    qt_com = []
    qt_rej = []
    # PSQL Queries
    # total enquires
    qtcount = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(
        Date__contains='2022-02') | Q(Date__contains='2022-03')).count()
    qtcount1 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(
        Date__contains='2022-05') | Q(Date__contains='2022-06')).count()
    qtcount2 = RY_Enquiry_Header.objects.filter(
        Q(Date__contains='2022-07') | Q(Date__contains='2022-08')).count()
    qt_total.append(qtcount)
    qt_total.append(qtcount1)
    qt_total.append(qtcount2)
    # enquires status for 0 ---- New Enquiry
    qtsts = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(
        Date__contains='2022-02') | Q(Date__contains='2022-03')).filter(Status__exact='0').count()
    qtcount12 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(
        Date__contains='2022-05') | Q(Date__contains='2022-06')).filter(Status__exact='0').count()
    qtcount22 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-07') | Q(
        Date__contains='2022-08')).filter(Status__exact='0').count()
    qt_0.append(qtsts)
    qt_0.append(qtcount12)
    qt_0.append(qtcount22)
    # enquires status for 3,6,12 ---- External
    qtsts = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(Date__contains='2022-02') | Q(
        Date__contains='2022-03')).filter(Q(Status__exact='6') | Q(Status__exact='12') | Q(Status__exact='3')).count()
    qtsts1 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(Date__contains='2022-05') | Q(
        Date__contains='2022-06')).filter(Q(Status__exact='6') | Q(Status__exact='12') | Q(Status__exact='3')).count()
    qtsts2 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-07') | Q(
        Date__contains='2022-08')).filter(Q(Status__exact='6') | Q(Status__exact='12') | Q(Status__exact='3')).count()
    qt_ex.append(qtsts)
    qt_ex.append(qtsts1)
    qt_ex.append(qtsts2)

    qtsts51 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(Date__contains='2022-02') | Q(Date__contains='2022-03')).filter(Q(Status__exact='1') | Q(
        Status__exact='2') | Q(Status__exact='5') | Q(Status__exact='7') | Q(Status__exact='8') | Q(Status__exact='9') | Q(Status__exact='10') | Q(Status__exact='11') | Q(Status__exact='13') | Q(Status__exact='4')).count()
    qtsts52 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(Date__contains='2022-05') | Q(Date__contains='2022-06')).filter(Q(Status__exact='1') | Q(
        Status__exact='2') | Q(Status__exact='5') | Q(Status__exact='7') | Q(Status__exact='8') | Q(Status__exact='9') | Q(Status__exact='10') | Q(Status__exact='11') | Q(Status__exact='13') | Q(Status__exact='4')).count()
    qtsts53 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-07') | Q(Date__contains='2022-08')).filter(Q(Status__exact='1') | Q(Status__exact='2') | Q(
        Status__exact='5') | Q(Status__exact='7') | Q(Status__exact='8') | Q(Status__exact='9') | Q(Status__exact='10') | Q(Status__exact='11') | Q(Status__exact='13') | Q(Status__exact='4')).count()
    qt_in.append(qtsts51)
    qt_in.append(qtsts52)
    qt_in.append(qtsts53)
    #  enquires status for -1 ---- Rejected
    qtsts71 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(
        Date__contains='2022-02') | Q(Date__contains='2022-03')).filter(Status__exact='-1').count()
    qtsts72 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(
        Date__contains='2022-05') | Q(Date__contains='2022-06')).filter(Status__exact='-1').count()
    qtsts73 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-07') | Q(
        Date__contains='2022-08')).filter(Status__exact='-1').count()
    qt_rej.append(qtsts71)
    qt_rej.append(qtsts72)
    qt_rej.append(qtsts73)
    # enquires status for 14 ---- Completed
    qtsts01 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-01') | Q(
        Date__contains='2022-02') | Q(Date__contains='2022-03')).filter(Status__exact='14').count()
    qtsts02 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-04') | Q(
        Date__contains='2022-05') | Q(Date__contains='2022-06')).filter(Status__exact='14').count()
    qtsts03 = RY_Enquiry_Header.objects.filter(Q(Date__contains='2022-07') | Q(
        Date__contains='2022-08')).filter(Status__exact='14').count()
    qt_com.append(qtsts01)
    qt_com.append(qtsts02)
    qt_com.append(qtsts03)
    res1 = request.COOKIES.get('username')
    #array for items
    type_name=[]
    items_values=[]
    items_no=RY_Enquiry_Items.objects.values('Type').annotate(Count('id')).order_by().filter(id__count__gt=0)
    for itm in items_no:
        type_name.append(itm['Type'])
        items_values.append(itm['id__count'])
    return render(request, 'app/graph.html',{'segment':'dashboard','Role':vLoggedInRole,'user':res1,'type_name': type_name, 'items_values':items_values, 'enquiry': count, 'completed': completed, 'inprocess': inprocess, 'rejected': rejected,'totalenq' : totaleq,'mon_0': mon_0, 'mon_in':mon_in,'mon_ex': mon_ex, 'mon_com':mon_com, 'rej':rej, 'qt_total' :qt_total, 'qt_0':qt_0 ,'qt_in' :qt_in ,'qt_ex' :qt_ex ,'qt_com':qt_com ,'qt_rej':qt_rej })

def Upload(request):
    res1 = request.COOKIES.get('username')
    vLoggedInRole = request.COOKIES.get('role')
    return render(request, 'app/Upload.html',{'user':res1,'segment':'Upload','Role':vLoggedInRole})

def groupDelete(request,id):
    res=Email_Distribution_Groups.objects.get(id=id)
    res.delete()
    return HttpResponseRedirect('/group')

def NewEntry(request):
    res1 = request.COOKIES.get('username')
    return render(request, 'app/ryn3.html',{'user':res1})

def NewEnquiry(request):
        vRowCount = 0
        if (request.POST.get('txtRowCount') != None):
            vRowCount = int(request.POST.get('txtRowCount'))

        for itemIndex in range(vRowCount):
            vRowIndex = itemIndex+1
            DBItemID = request.POST.get('DBID'+str(vRowIndex))
            vRowIndex = itemIndex+1
            vCounts = request.POST.get('Counts'+str(vRowIndex))
            vQuality = request.POST.get('Quality'+str(vRowIndex))
            vYarnType = request.POST.get('YarnType'+str(vRowIndex))
            vBlend = request.POST.get('Blend'+str(vRowIndex))
            vShade = request.POST.get('Shade'+str(vRowIndex))   
            vDepth = request.POST.get('Depth'+str(vRowIndex))
            vUOM = request.POST.get('UOM'+str(vRowIndex))
            vQuantity = request.POST.get('Quantity'+str(vRowIndex))
            vDAO.StoreNewEnquiry(vCounts, vQuality, vYarnType, vBlend, vShade, vDepth,
                                vQuantity, vUOM)
        return HttpResponseRedirect('/NewEntry')


def Errors(request):
        return render(request, 'app/Error.html')
    