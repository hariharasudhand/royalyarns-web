# Generated by Django 4.0.2 on 2022-08-12 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantity_details',
            name='Dark1',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='quantity_details',
            name='Light1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='quantity_details',
            name='OverDyed',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='quantity_details',
            name='White1',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
