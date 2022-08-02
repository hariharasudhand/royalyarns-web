from pyexpat import model
from django.db import models
from django.contrib.auth.models import User


class Dispatch_Header(models.Model):
    id = models.AutoField(primary_key=True)
    Link_ID = models.TextField(max_length=50,  null=True)
    Excel_Sheet_Name = models.TextField(max_length=200,  null=True)

    class Meta:
        db_table = 'Dispatch_Header'
        ordering = ['Link_ID']

    def __str__(self):
        return self.Link_ID + ' ' + self.Link_ID + ' ' + self.Excel_Sheet_Name + '' + self.Id


class Dispatch_Excel_Dump(models.Model):
    id = models.AutoField(primary_key=True)
    Link_ID = models.TextField(max_length=50,  null=True)
    Link_Header_ID = models.TextField(max_length=50,  null=True)
    DataKey = models.TextField(max_length=500,  null=True)
    DataValue = models.TextField(max_length=500,  null=True)

    class Meta:
        db_table = 'Dispatch_Excel_Dump'
        ordering = ['Link_ID']

    def __str__(self):
        return self.id + ' ' + self.Link_ID + ' ' + self.DataKey + '' + self.DataValue
