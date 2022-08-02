from .models import RY_Enquiry_Header, RY_Enquiry_Items, User_Details, customer_comments, User_Role_Action, Upload_Data
from django.db.models import Q
from .ExcelUtlis import ExcelUtlis


class DAO:

    name = ''

    def __init__(self, name):
        self.name = name

    ##
    # GetLandingPageData gets the overall enquiries
    # TO:DO This has to be modified to query enquiries related
    # to logined in Role Agent or Supplier or Buyer
    ##

    ##
# GetLandingPageData gets the overall enquiries
# TO:DO This has to be modified to query enquiries related
# to logined in Role Agent or Supplier or Buyer
##

    def GetLandingPageData(self, vLoggedInUserID, vLoggedInRole):

        # context = {'Error': 'No data found'}
        context = {}
        Unread_Data = []
        other_status = []
        Req_Yarn_Price = []
        Ready_for_Quote = []

        if (vLoggedInRole == 'agent'):
            # Query and Fetch only status that an AGENT should see
            Unread_Data = RY_Enquiry_Header.objects.filter(Status='0')
            Internal_Review = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='3') & ~Q(Status='4') & ~Q(Status='5') & ~Q(Status='6'))
            # & ~Q(Status='4')
            Req_Yarn_Price = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(Status='2') & ~Q(Status='5') & ~Q(Status='6'))
            Ready_for_Quote = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(Status='2') & ~Q(Status='3') & ~Q(Status='4'))

        elif (vLoggedInRole == 'supplier'):
            # Query and Fetch only status that an SUPPLIER should see
            Unread_Data = RY_Enquiry_Header.objects.filter(Status='3')
            Internal_Review = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(
                    Status='2') & ~Q(Status='3')
                & ~Q(Status='4') & ~Q(Status='5') & ~Q(Status='6'))
            Req_Yarn_Price = RY_Enquiry_Header.objects.filter(Status='4')
            Ready_for_Quote = RY_Enquiry_Header.objects.filter(Status='5')
        else:
            # Query and Fetch only status that an BUYER should see
            Unread_Data = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(
                    Status='2') & ~Q(Status='3')
                & ~Q(Status='4') & ~Q(Status='5'))
            Internal_Review = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(
                    Status='2') & ~Q(Status='3')
                & ~Q(Status='4') & ~Q(Status='5') & ~Q(Status='6'))
            Req_Yarn_Price = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(
                    Status='2') & ~Q(Status='3')
                & ~Q(Status='4') & ~Q(Status='5') & ~Q(Status='6'))
            Ready_for_Quote = RY_Enquiry_Header.objects.filter(
                ~Q(Status='0') & ~Q(Status='1') & ~Q(
                    Status='2') & ~Q(Status='3')
                & ~Q(Status='4') & ~Q(Status='5') & ~Q(Status='6'))

        Count_Unr = str(len(Unread_Data))
        Count_RYP = str(len(Req_Yarn_Price))
        Count_RFQ = str(len(Ready_for_Quote))
        Count_Others = str(len(Internal_Review))

        context['Unread('+Count_Unr+')'] = Unread_Data
        context['YarnPrice('+Count_RYP+')'] = Req_Yarn_Price
        context['ForQuote('+Count_RFQ+')'] = Ready_for_Quote
        context['InternalReview('+Count_Others+')'] = Internal_Review
        context['user'] = vLoggedInUserID
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
    def GetComments(self, vReg_no, vLoggedInRole):
        print('vLoggedInRole', vLoggedInRole)
        if (vLoggedInRole == 'agent'):
            return customer_comments.objects.filter(Reg_no=vReg_no).filter(
                ~Q(Commments_to="buyer2") & ~Q(Commments_to="supplier2") & ~Q(Commments_to="buyer3") & ~Q(Commments_to="supplier3"))
        elif (vLoggedInRole == 'supplier'):
            print("inside supplier", vLoggedInRole)
            return customer_comments.objects.filter(Reg_no=vReg_no).filter(
                ~Q(Commments_to="agent1") & ~Q(Commments_to="buyer1") & ~Q(Commments_to="buyer2") & ~Q(Commments_to="agent2"))

        else:
            print("inside Buyer", vLoggedInRole)
            return customer_comments.objects.filter(Reg_no=vReg_no).filter(
                ~Q(Commments_to="agent1") & ~Q(Commments_to="supplier1") & ~Q(Commments_to="agent3") & ~Q(Commments_to="supplier3"))
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

    def StoreEnquiryItem(self, vDBItemID, vReg_no, vCounts, vQuality, vType, vBlend, vShade, vDepth, vUOM, vQuantity, vSupplier_Rate, vSupplier_Amount, vSupplier_Last_order, vStatus, vDBFlag, vARate, vAAmount, vALast_order, vUserID, vNow):

        if (vDBFlag == 1):
            RY_Enquiry_Items.objects.filter(id=vDBItemID, Reg_no=vReg_no).update(
                Counts=vCounts, Quality=vQuality, Type=vType, Blend=vBlend, Shade=vShade, Depth=vDepth, UOM=vUOM, Quantity=vQuantity, Supplier_Rate=vSupplier_Rate, Supplier_Amount=vSupplier_Amount, Supplier_Last_order=vSupplier_Last_order, Agent_Rate=vARate, Agent_Amount=vAAmount,
                Agent_Last_order=vALast_order, Status=vStatus, CreatedByUser='RPABOT', LastUpdateby=vUserID, LastUpdateddate=vNow)

        else:

            ryNewItem = RY_Enquiry_Items(Reg_no=vReg_no, Counts=vCounts, Quality=vQuality, Type=vType, Blend=vBlend, Shade=vShade,
                                         Depth=vDepth, UOM=vUOM, Quantity=vQuantity, Supplier_Rate=vSupplier_Rate, Supplier_Amount=vSupplier_Amount,
                                         Supplier_Last_order=vSupplier_Last_order, Agent_Rate=vARate, Agent_Amount=vAAmount, Agent_Last_order=vALast_order,
                                         Status=vStatus, CreatedByUser='RPABOT', LastUpdateby=vUserID, LastUpdateddate=vNow)
            ryNewItem.save()

    def StoreEnquiryHeader(self, vReg_no, vMill, vDate, vMill_Rep, vCustomer, vMarketing_Zone, vStatus, vUser, vNow):
        # TO:DO Header is always an update - this has to check if there is a change only then this should be
        # updated
        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(
            Mill=vMill, Date=vDate, Mill_Rep=vMill_Rep, Customer=vCustomer, Marketing_Zone=vMarketing_Zone, Status=vStatus, LastUpdateby=vUser, LastUpdateddate=vNow)

    def StoreComments(self, vComments, vReg_no, vUserID, vDT, vComments_to):
        customer_comments.objects.create(
            Comments=vComments, Reg_no=vReg_no, Commments_to=vComments_to, DT=vDT, CreatedByUser=vUserID, Created_Date=vDT)

    def UpdateEnquiryStatus(self, vReg_no, vStatus):

        RY_Enquiry_Items.objects.filter(Reg_no=vReg_no).update(Status=vStatus)
        RY_Enquiry_Header.objects.filter(Reg_no=vReg_no).update(Status=vStatus)

    def GetUserActionByRole(self, vLoggedInRole, vStatus):

        return User_Role_Action.objects.filter(Role=vLoggedInRole).filter(Status=vStatus)
    #
    # Get for ExcelFile
    #

    def GetUpload_Data(self, Upload):

        return User_Role_Action.objects.filter(Upload_file=Upload)

    #
    # Upload for ExcelFile
    #
    def StoreUpload_Data(self, vExcelPath, vDate, vUser):

        vExcelFileURL = "/Users/harid/work/weeroda/RoyalYarns/teratta-app/media/"+vExcelPath.name
        print('Processing Upload Excel File Name : ', vExcelFileURL)

        excelUtil = ExcelUtlis(vExcelFileURL)

        Upload_Data.objects.create(
            Upload_file=vExcelPath, Date=vDate, Upload_by=vUser, Upload_Status='1', Process_Status='0'
        )
        print("Excel File Uploaded in location : ", vExcelFileURL)
        print(excelUtil.GetInsertQueryList(vExcelFileURL))
