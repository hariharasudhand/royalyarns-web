from .models import RY_Enquiry_Header, RY_Enquiry_Items, User_Details, customer_comments
from django.db.models import Q


class DAO:

    name = ''

    def __init__(self, name):
        self.name = name

    ##
    # GetLandingPageData gets the overall enquiries
    # TO:DO This has to be modified to query enquiries related
    # to logined in Role Agent or Supplier or Buyer
    ##

    def GetLandingPageData(self):

        # context = {'Error': 'No data found'}
        context = {}
        Unread_Data = RY_Enquiry_Header.objects.filter(Status='0')
        other_status = RY_Enquiry_Header.objects.filter(
            ~Q(Status='0') & ~Q(Status='3') & ~Q(Status='4'))
        Req_Yarn_Price = RY_Enquiry_Header.objects.filter(Status='3')
        Ready_for_Quote = RY_Enquiry_Header.objects.filter(Status='4')

        Count_Unr = str(len(Unread_Data))
        Count_RYP = str(len(Req_Yarn_Price))
        Count_RFQ = str(len(Ready_for_Quote))
        Count_Others = str(len(other_status))

        context['Unread('+Count_Unr+')'] = Unread_Data
        context['YarnPrice('+Count_RYP+')'] = Req_Yarn_Price
        context['ForQuote('+Count_RFQ+')'] = Ready_for_Quote
        context['Others('+Count_Others+')'] = other_status

        context['full'] = context

        return context
    ##
    # GetEnquiryHeader
    # Wrapper method that fetches enquiry header details of supplied Reg_No
    # TO:DO Check if the logged in Role has access to the Reg_No
    ##

    def GetEnquiryHeader(self, vReg_no):
        return RY_Enquiry_Header.objects.filter(Reg_no=vReg_no)

    ##
    # GetEnquiryItems
    # Wrapper method that fetches enquiry items details of supplied Reg_No
    # TO:DO Check if the logged in Role has access to the Reg_No
    ##
    def GetEnquiryItems(self, vReg_no):
        return RY_Enquiry_Items.objects.filter(Reg_no=vReg_no)

    ##
    # GetComments
    # Wrapper method that fetches enquiry comments details of supplied Reg_No
    # TO:DO Check if the logged in Role has access to the comments
    ##
    def GetComments(self, vReg_no):
        return customer_comments.objects.filter(Reg_no=vReg_no)

     ##
    # GetUserInfo
    # Wrapper method that fetches userinfo
    ##
    def GetUserInfo(self, vUser, vPassword):
        return User_Details.objects.filter(
            UserName=vUser, Password=vPassword)
    ##
    # StoreEnquiry wrapper method that
    # Updates Enquiry Header
    # Inserts or Updates Enquiry Items - based on vDBFlag
    # if vDBFlag = 1 (updates)
    # if vDBFlag = 0 inserts new entry
    ##

    def StoreEnquiryItem(self, vDBItemID, vReg_no, vCounts, vQuality, vType, vBlend, vShade, vDepth, vUOM, vQuantity, vSupplier_Rate, vSupplier_Amount, vSupplier_Last_order, vStatus, vDBFlag):

        if (vDBFlag == 1):
            RY_Enquiry_Items.objects.filter(id=vDBItemID, Reg_no=vReg_no).update(
                Counts=vCounts, Quality=vQuality, Type=vType, Blend=vBlend, Shade=vShade, Depth=vDepth, UOM=vUOM, Quantity=vQuantity, Supplier_Rate=vSupplier_Rate, Supplier_Amount=vSupplier_Amount, Supplier_Last_order=vSupplier_Last_order, Status=vStatus)

        else:

            ryNewItem = RY_Enquiry_Items(Reg_no=vReg_no, Counts=vCounts, Quality=vQuality, Type=vType, Blend=vBlend, Shade=vShade,
                                         Depth=vDepth, UOM=vUOM, Quantity=vQuantity, Supplier_Rate=vSupplier_Rate, Supplier_Amount=vSupplier_Amount, Supplier_Last_order=vSupplier_Last_order, Status=vStatus)
            ryNewItem.save()

    def StoreEnquiryHeader(self, vReg_no, vMill, vDate, vMill_Rep, vCustomer, vMarketing_Zone, vStatus):
        # TO:DO Header is always an update - this has to check if there is a change only then this should be
        # updated
        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
            Mill=vMill, Date=vDate, Mill_Rep=vMill_Rep, Customer=vCustomer, Marketing_Zone=vMarketing_Zone, Status=vStatus)

    def StoreComments(self, vCommand, vReg_no, vCustomer, vDT):
        customer_comments.objects.create(
            Comments=vCommand, Reg_no=vReg_no, UserId=vCustomer, DT=vDT)

    def UpdateEnquiryStatus(self, vReg_no, vStatus):

        RY_Enquiry_Items.objects.filter(Reg_no=vReg_no).update(Status=vStatus)
        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(Status=vStatus)
