# Generated by Django 4.0.2 on 2022-07-25 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0004_customer_comments_createdbyuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer_comments',
            old_name='LastUpdateby',
            new_name='Created_Date',
        ),
        migrations.RemoveField(
            model_name='customer_comments',
            name='LastUpdateddate',
        ),
    ]