from itertools import count
from django.db import models

# Create your models here.


class RY_Enquiry_Items(models.Model):
    Counts = models.TextField(max_length=200)
    Quality = models.TextField(max_length=200)
    Type = models.TextField(max_length=200)
    Blend = models.TextField(max_length=200)
    Shade = models.TextField(max_length=200)
    Shade_Ref = models.TextField(max_length=200)
    Depth = models.TextField(max_length=200)
    UOM = models.TextField(max_length=200)
    Quantity = models.TextField(max_length=200)
    Status = models.TextField(max_length=200)
    Reg_no = models.IntegerField(max_length=200)
    Id = models.IntegerField(max_length=200)

    class Meta:
        db_table = 'RY_Enquiry_Items'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Counts + ' ' + self.Quality + ' ' + self.Type + ' ' + self.Blend + ' ' + self.Shade + ' ' + self.Shade_Ref + ' ' + self.Depth + ' ' + self.UOM + ' ' + self.Quantity + ' ' + self.Reg_no + ' ' + self.Status + '' + self.Id


class RY_Enquiry_Header(models.Model):
    # Id = models.IntegerField(max_length=200)
    Reg_no = models.IntegerField(max_length=200)
    Mill = models.TextField(max_length=200)
    Mill_Rep = models.TextField(max_length=200)
    Customer = models.TextField(max_length=200)
    Marketing_Zone = models.TextField(max_length=200)
    Payment_Term = models.TextField(max_length=200)
    Narration = models.TextField(max_length=200)
    Reason_For_Non_Acception = models.TextField(max_length=200)
    Replied_From_the_mill = models.TextField(max_length=200)
    Acceptance_from_the_mill = models.TextField(max_length=200)
    Date = models.TextField(max_length=200)
    Email_Details = models.TextField(max_length=200)
    Status = models.TextField(max_length=200)

    class Meta:
        db_table = 'RY_Enquiry_Header'
        ordering = ['Reg_no']

    def __str__(self):
        return self.Reg_no + ' ' + self.Mill + ' ' + self.Customer + ' ' + self.Marketing_Zone + ' ' + self.Payment_Term + ' ' + self.Narration + ' ' + self.Reason_For_Non_Acception + ' ' + self.Reason_For_Non_Acception + ' ' + self.Acceptance_from_the_mill + ' ' + self.Date + '' + self.Email_Details


# class Email(models.Model):
#     Email_content = models.TextField(max_length=1000)

#     class Meta:
#         db_table = 'app_customer'

#     def __str__(self):
#         return self.Email_content
