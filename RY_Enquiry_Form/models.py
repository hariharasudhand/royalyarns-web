from pyexpat import model
from django.db import models
from django.contrib.auth.models import User


class RY_Enquiry_Items(models.Model):
    # Id = models.IntegerField(null=True)
    Counts = models.TextField(max_length=200,  null=True)
    Quality = models.TextField(max_length=200,  null=True)
    Type = models.TextField(max_length=200,  null=True)
    Blend = models.TextField(max_length=200,  null=True)
    Shade = models.TextField(max_length=200,  null=True)
    Shade_Ref = models.TextField(max_length=200,  null=True)
    Depth = models.TextField(max_length=200,  null=True)
    UOM = models.TextField(max_length=200, null=True)
    Quantity = models.TextField(max_length=200,  null=True)
    Status = models.TextField(max_length=200,  null=True)
    Reg_no = models.TextField(max_length=200,  null=True)
    Supplier_Rate = models.ImageField(max_length=200,  null=True)
    Supplier_Amount = models.ImageField(max_length=200,  null=True)
    Supplier_Last_order = models.TextField(max_length=200,  null=True)
    Agent_Rate = models.ImageField(max_length=200,  null=True)
    Agent_Amount = models.ImageField(max_length=200,  null=True)
    Agent_Last_order = models.TextField(max_length=200,  null=True)
    CreatedByUser = models.TextField(max_length=200, null=True)
    LastUpdateby = models.TextField(max_length=200, null=True)
    LastUpdateddate = models.TextField(max_length=200, null=True)

    class Meta:
        db_table = 'RY_Enquiry_Items'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Agent_Rate + ' ' + self.Agent_Amount + ' ' + self.Agent_Last_order + self.Supplier_Rate + ' ' + self.Supplier_Amount + ' ' + self.Supplier_Last_order + ' ' + self.Counts + ' ' + self.Quality + ' ' + self.Type + ' ' + self.Blend + ' ' + self.Shade + ' ' + self.Shade_Ref + ' ' + self.Depth + ' ' + self.UOM + ' ' + self.Quantity + ' ' + self.Reg_no + ' ' + self.Status + '' + self.Id


class RY_Enquiry_Header(models.Model):
    # Id = models.IntegerField(max_length=200)
    Reg_no = models.TextField(max_length=200,  null=True)
    Mill = models.TextField(max_length=200,  null=True)
    Mill_Rep = models.TextField(max_length=200, null=True)
    Customer = models.TextField(max_length=200,  null=True)
    Marketing_Zone = models.TextField(max_length=200,  null=True)
    Payment_Term = models.TextField(max_length=200,  null=True)
    Narration = models.TextField(max_length=200,  null=True)
    Reason_For_Non_Acception = models.TextField(
        max_length=200,  null=True)
    Replied_From_the_mill = models.TextField(
        max_length=200, null=True)
    Acceptance_from_the_mill = models.TextField(
        max_length=200,  null=True)
    Date = models.TextField(max_length=200,  null=True)
    Email_Details = models.TextField(max_length=200,  null=True)
    Status = models.TextField(max_length=200, null=True)
    CreatedByUser = models.TextField(max_length=200, null=True)
    LastUpdateby = models.TextField(max_length=200, null=True)
    LastUpdateddate = models.TextField(max_length=200, null=True)
    Po_Number = models.CharField(max_length=100, null=True)
    Po_Date = models.CharField(max_length=100, null=True)
    Po_PDF = models.FileField(max_length=500, null=True)
    Po_RevDate = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'RY_Enquiry_Header'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Mill_Rep + ' ' + self.Reg_no + ' ' + self.Mill + ' ' + self.Customer + ' ' + self.Marketing_Zone + ' ' + self.Payment_Term + ' ' + self.Narration + ' ' + self.Reason_For_Non_Acception + ' ' + self.Reason_For_Non_Acception + ' ' + self.Acceptance_from_the_mill + ' ' + self.Date + '' + self.Email_Details + ' ' + self.Status



# class RY_Purcahse_Sales_Confirmation(models.Model):
#     # Id = models.IntegerField(null=True)
#     PC_no = models.TextField(max_length=200,  null=True)
#     SC_no = models.TextField(max_length=200,  null=True)
#     Cop_no = models.TextField(max_length=200,  null=True)
#     Reg_no = models.TextField(max_length=200,  null=True)
#     QD_Fab_FeederStripes = models.TextField(max_length=20,  null=True)
#     QD_Fab_Jacquard = models.TextField(max_length=20,  null=True)
#     QD_Fab_MiniJag = models.TextField(max_length=20,  null=True)
#     QD_Fab_Auto_Stripes = models.TextField(max_length=20,  null=True)
#     QD_Fab_SingleJersey = models.TextField(max_length=20,  null=True)
#     QD_Fab_PbyK = models.TextField(max_length=20,  null=True)
#     QD_Fab_Interlock = models.TextField(max_length=20,  null=True)
#     QD_Fab_Rib = models.TextField(max_length=20,  null=True)
#     QD_Fab_DyeingWhite = models.TextField(max_length=20,  null=True)
#     QD_Fab_DyeingLight = models.TextField(max_length=20,  null=True)
#     QD_Fab_DyeingMedium = models.TextField(max_length=20,  null=True)
#     QD_Fab_DyeingDark = models.TextField(max_length=20,  null=True)
#     QD_Fab_OtherWhite = models.TextField(max_length=20,  null=True)
#     QD_Fab_OtherLight = models.TextField(max_length=20,  null=True)
#     QD_Fab_OtherMedium = models.TextField(max_length=20,  null=True)
#     QD_Fab_OtherDark = models.TextField(max_length=20,  null=True)
#     QD_PayMode = models.TextField(max_length=20,  null=True)
#     QD_PayRS = models.TextField(max_length=20,  null=True)
#     QD_PayNo = models.TextField(max_length=200,  null=True)
#     QD_PayDate = models.TextField(max_length=50,  null=True)
#     QD_PayBank = models.TextField(max_length=200,  null=True)

#     class Meta:
#         db_table = 'RY_Purcahse_Sales_Confirmation'
#         ordering = ['Reg_no']

#     def __str__(self):
#         return ''


class User_Details(models.Model):
    id = models.IntegerField(primary_key=True)
    UserName = models.TextField(max_length=200,  null=True)
    Password = models.TextField(max_length=200,  null=True)
    Role = models.TextField(max_length=200,  null=True)
   

    class Meta:
        db_table = 'User_Details'
        ordering = ['Role']

    def __str__(self):
        return self.UserName


class customer_comments(models.Model):
    id = models.AutoField(primary_key=True)
    Commments_to = models.TextField(max_length=100,  null=True)
    Comments = models.TextField(max_length=200,  null=True)
    Reg_no = models.TextField(max_length=200,  null=True)
    DT = models.TextField(max_length=200,  null=True)
    CreatedByUser = models.TextField(max_length=100, null=True)
    Created_Date = models.TextField(max_length=100, null=True)

    class Meta:
        db_table = 'customer_comments'
        ordering = ['DT']

    def __str__(self):
        return self.id + ' ' + self.UserId + ' ' + self.Comments + ' ' + self.Reg_no + ' ' + self.DT


class purchase(models.Model):
    id = models.AutoField(primary_key=True)
    pono = models.CharField(max_length=200, null=True)
    popdf = models.FileField(max_length=500, null=True)

    class Meta:
        db_table = 'purchase_details'


class User_Role_Action(models.Model):
    id = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=10, null=True)
    Status = models.CharField(max_length=10, null=True)
    Action = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'User_Role_Action'


class Upload_Data(models.Model):
    id = models.AutoField(primary_key=True)
    Upload_file = models.FileField(max_length=300, null=True)
    Date = models.CharField(max_length=100,  null=True)
    Upload_by = models.CharField(max_length=100, null=True)
    Upload_Status = models.CharField(max_length=2, null=True)
    Process_Status = models.CharField(max_length=2, null=True)

    class Meta:
        db_table = 'Upload_data'

    

class Email_Distribution_Groups(models.Model):
    id = models.AutoField(primary_key=True)
    GroupName = models.CharField(max_length=100, null=True)
    GroupUsersID = models.CharField(max_length=100, null=True)
    Status = models.BooleanField(max_length=10, null=True)
   
   
   

    class Meta:
        db_table = 'Email_Distribution_Groups'

class Other_Details(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_Schedule = models.CharField(max_length=100, null=True)
    payment_term = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    matching_source = models.CharField(max_length=100, null=True)
    buyer = models.CharField(max_length=100, null=True)
    any_other_specification = models.CharField(max_length=100, null=True)
    specification_if_no_product_type = models.CharField(max_length=100, null=True)
    commision = models.CharField(max_length=100, null=True)
    Baby_cone = models.BooleanField(max_length=10, null=True)
    air = models.BooleanField(max_length=10, null=True)
    Reg_no = models.CharField(max_length=200,  null=True)

   
   
   

    class Meta:
        db_table = 'Other_Details'

class Quantity_Details(models.Model):
    id = models.AutoField(primary_key=True)
    feeder_stripes = models.CharField(max_length=100, null=True)
    jacaquard = models.CharField(max_length=100, null=True)
    mini_jaq = models.CharField(max_length=10, null=True)
    auto_stripes = models.CharField(max_length=100, null=True)
    single_jersey = models.CharField(max_length=100, null=True)
    p_k = models.CharField(max_length=10, null=True)
    interlock = models.CharField(max_length=100, null=True)
    rib = models.CharField(max_length=100, null=True)
    white = models.CharField(max_length=10, null=True)
    light = models.CharField(max_length=100, null=True)
    medium = models.CharField(max_length=100, null=True)
    dark = models.CharField(max_length=10, null=True)
    pay_mode = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=10, null=True)
    date = models.DateField(max_length=100, null=True)
    bank = models.CharField(max_length=100, null=True)
    Reg_no = models.CharField(max_length=200,  null=True)

    class Meta:
        db_table = 'Quantity_Details'

#ROCKETBOT TABLES CREATES HERE

class Customer_Name(models.Model):
    id = models.AutoField(primary_key=True)
    customer_names =  models.TextField(max_length=200,  null=True)
    customer_emailid = models.TextField(max_length=200,  null=True)
    splited_details =  models.TextField(max_length=200,  null=True)


    class Meta:
        db_table = 'Customer_Name'


class Duplication(models.Model):
    id = models.AutoField(primary_key=True)
    Count = models.TextField(max_length=200,  null=True)
    Blend = models.TextField(max_length=200,  null=True)
    Shade_Ref = models.TextField(max_length=200,  null=True)
    Quantity = models.TextField(max_length=200,  null=True)


    class Meta:
        db_table = 'Duplication'


class ShadeRef_With_mill(models.Model):
    id = models.AutoField(primary_key=True)
    shade_ref = models.TextField(max_length=200,  null=True)
    shade = models.TextField(max_length=200,  null=True)
    type = models.TextField(max_length=200,  null=True)
    mill = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'ShadeRef_With_mill'

class items_to_mill_mapping(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.TextField(max_length=200,  null=True)
    mill = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'items_to_mill_mapping'


     


    

