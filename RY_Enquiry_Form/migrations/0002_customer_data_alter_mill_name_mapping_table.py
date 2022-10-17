# Generated by Django 4.0.2 on 2022-10-17 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RY_Enquiry_Form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Columns_names', models.TextField(max_length=500, null=True)),
                ('Customer_name', models.TextField(max_length=500, null=True)),
                ('payment_terms', models.TextField(max_length=500, null=True)),
                ('splitted_details', models.TextField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'customer_data',
            },
        ),
        migrations.AlterModelTable(
            name='mill_name_mapping',
            table='mill_name_mapping',
        ),
    ]
