# Generated by Django 4.0.2 on 2022-10-07 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0002_ry_enquiry_header_delivery_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload_data',
            name='Upload_file',
            field=models.FileField(max_length=5000, null=True, upload_to=''),
        ),
    ]
