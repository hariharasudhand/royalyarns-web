# Generated by Django 4.0.2 on 2022-08-02 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0009_upload_data_alter_purchase_popdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload_data',
            name='Date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='upload_data',
            name='Last_Status',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='upload_data',
            name='Process',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='upload_data',
            name='Upload_by',
            field=models.CharField(max_length=30, null=True),
        ),
    ]