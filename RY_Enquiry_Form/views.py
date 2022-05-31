from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from psycopg2 import Date
from .forms import Ry_En_Form, Ry_En_Header
from .models import RY_Enquiry_Header, RY_Enquiry_Items
import subprocess


def index(request):
    vReg_no = request.GET.get('Rno')
    data = RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)
    data2 = RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)
    vFlag = request.POST.get('Rno')
    if vFlag != None:
        data = RY_Enquiry_Items.objects.filter(Reg_no=vFlag)
        data2 = RY_Enquiry_Header.objects.filter(Reg_no=vFlag)
        update_book(request, data, vReg_no, data2)
        # print("*********vFlag", vFlag)
    # if request.method == 'POST':
    #     form = Ry_En_Form(request.POST)
    #     if request.POST.get("Save"):
    #         data = RY_Enquiry_Items.objects.filter(Reg_no=vFlag)
    #         print("save botton is clicked")
    #         update_status(request, data, vReg_no)
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

            print("data from database Counts :", Counts)

        context = {'form': form,
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
                   'Customer': Customer

                   }
    else:
        context = {'Error': 'No data found'
                   }

    return render(request, 'app/ryn2.html', context)


def update_book(request, data, vReg_no, data2):
    # print("*******************", request.POST.get('Rno'))
    # GET txtcancel HIDDEN FIELD VALUE, IF CANCEL BUTTON IS CLICKED
    # THE HIDDEN FIELD WILL HAVE VALUE OR ELSE EMPTY IS SAVE BUTTON IS CLICKED

    visCancel = request.POST.get('txtcancel')
    
    if len(visCancel) == 0:
      # IF SAVE BUTTON IS CLICKED CANCEL HIDDEN FIELD WILL BE EMPTY  
      for item in data:
            vid = str(item.id)
            RY_Enquiry_Items.objects.filter(id=vid).update(
                Counts=request.POST.get('Counts'+str(item.id)), Quality=request.POST.get('Quality'+str(item.id)), Type=request.POST.get('YarnType'+str(item.id)), Blend=request.POST.get('Blend'+str(item.id)), Shade=request.POST.get('Shade'+str(item.id)), Depth=request.POST.get('Depth'+str(item.id)), UOM=request.POST.get('UOM'+str(item.id)), Quantity=request.POST.get('Quantity'+str(item.id)), Status=1)

      RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
            Mill=request.POST.get('Mill'), Date=request.POST.get('Date'), Mill_Rep=request.POST.get('Mill_Rep'), Customer=request.POST.get('Customer'), Marketing_Zone=request.POST.get('Marketing_Zone'),Status=1)
    else:
        #IF CANCEL BUTTON IS CLICKED , HIDDEN FIELD WILL HAVE VALUE AND HENCE THIS BLOCK WILL 
        # BE EXECUTED
        for item in data:
            vid = str(item.id)
            RY_Enquiry_Items.objects.filter(id=vid).update(Status=2)

        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(Status=2)
    

    
    # subprocess.call([r'C:/Rocketbot/Rocketbot/rocketbot_launcher.bat'])
    return render(request, 'app/ryn2.html', {'upload_form': Ry_En_Form})


# def update_status(request, data, vReg_no):
#     for item in data:
#         vid = str(item.id)
#         RY_Enquiry_Items.objects.filter(id=vid).update(
#             Counts=request.POST.get('Counts'+str(item.id)), Quality=request.POST.get('Quality'+str(item.id)), Type=request.POST.get('YarnType'+str(item.id)), Blend=request.POST.get('Blend'+str(item.id)), Shade=request.POST.get('Shade'+str(item.id)), Depth=request.POST.get('Depth'+str(item.id)), UOM=request.POST.get('UOM'+str(item.id)), Quantity=request.POST.get('Quantity'+str(item.id)), Status=1)

#     RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
#         Mill=request.POST.get('Mill'), Date=request.POST.get('Date'), Mill_Rep=request.POST.get('Mill_Rep'), Customer=request.POST.get('Customer'), Marketing_Zone=request.POST.get('Marketing_Zone'))

#     return render(request, 'app/ryn.html', {'upload_form': Ry_En_Form})


def Data_Rno():
    data1 = RY_Enquiry_Header.objects.all()
    # data = Customer.objects.filter(Reg_no='411')

    for item in data1:
        Email_text = item.Email_Details
        print("data from database Email_text :", Email_text)
    return Email_text
