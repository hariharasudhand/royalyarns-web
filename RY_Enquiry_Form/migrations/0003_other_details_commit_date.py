# Generated by Django 4.0.2 on 2022-10-17 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0002_customer_data_alter_mill_name_mapping_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='other_details',
            name='Commit_date',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
