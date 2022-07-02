from django.db import models
from django.contrib.auth.models import User


class RY_Enquiry_Items(models.Model):
    Id = models.IntegerField(null=True)
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
    Rate = models.ImageField(max_length=200,  null=True)
    Amount = models.ImageField(max_length=200,  null=True)
    Last_order = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'RY_Enquiry_Items'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Rate + ' ' + self.Amount + ' ' + self.Last_order + ' ' + self.Counts + ' ' + self.Quality + ' ' + self.Type + ' ' + self.Blend + ' ' + self.Shade + ' ' + self.Shade_Ref + ' ' + self.Depth + ' ' + self.UOM + ' ' + self.Quantity + ' ' + self.Reg_no + ' ' + self.Status + '' + self.Id


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

    class Meta:
        db_table = 'RY_Enquiry_Header'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Mill_Rep + ' ' + self.Reg_no + ' ' + self.Mill + ' ' + self.Customer + ' ' + self.Marketing_Zone + ' ' + self.Payment_Term + ' ' + self.Narration + ' ' + self.Reason_For_Non_Acception + ' ' + self.Reason_For_Non_Acception + ' ' + self.Acceptance_from_the_mill + ' ' + self.Date + '' + self.Email_Details + ' ' + self.Status


class User_Details(models.Model):
    id = models.IntegerField(primary_key=True)
    UserName = models.TextField(max_length=200,  null=True)
    Password = models.TextField(max_length=200,  null=True)
    Role = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'User_Details'
        ordering = ['Role']

    def __str__(self):
        return self.id + ' ' + self.UserName + ' ' + self.Password + ' ' + self.Role


class customer_comments(models.Model):
    id = models.AutoField(primary_key=True)
    UserId = models.TextField(max_length=200,  null=True)
    Comments = models.TextField(max_length=200,  null=True)
    Reg_no = models.TextField(max_length=200,  null=True)
    DT = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'customer_comments'
        ordering = ['DT']

    def __str__(self):
        return self.id + ' ' + self.UserId + ' ' + self.Comments + ' ' + self.Reg_no + ' ' + self.DT
