# Generated by Django 4.0.2 on 2022-10-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer_comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Commments_to', models.TextField(max_length=100, null=True)),
                ('Comments', models.TextField(max_length=200, null=True)),
                ('Reg_no', models.TextField(max_length=200, null=True)),
                ('DT', models.TextField(max_length=200, null=True)),
                ('CreatedByUser', models.TextField(max_length=100, null=True)),
                ('Created_Date', models.TextField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'customer_comments',
                'ordering': ['DT'],
            },
        ),
        migrations.CreateModel(
            name='Customer_Name',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_names', models.TextField(max_length=200, null=True)),
                ('customer_emailid', models.TextField(max_length=200, null=True)),
                ('splited_details', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'Customer_Name',
            },
        ),
        migrations.CreateModel(
            name='Dispatch_Excel_Dump',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Link_ID', models.TextField(max_length=50, null=True)),
                ('Link_Header_ID', models.TextField(max_length=50, null=True)),
                ('Data_RowIndex', models.CharField(max_length=2, null=True)),
                ('DataKey', models.TextField(max_length=500, null=True)),
                ('DataValue', models.TextField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'Dispatch_Excel_Dump',
                'ordering': ['Link_ID'],
            },
        ),
        migrations.CreateModel(
            name='Dispatch_Header',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Link_ID', models.TextField(max_length=50, null=True)),
                ('Excel_Sheet_Name', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'Dispatch_Header',
                'ordering': ['Link_ID'],
            },
        ),
        migrations.CreateModel(
            name='Duplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Count', models.TextField(max_length=200, null=True)),
                ('Blend', models.TextField(max_length=200, null=True)),
                ('Shade_Ref', models.TextField(max_length=200, null=True)),
                ('Quantity', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'Duplication',
            },
        ),
        migrations.CreateModel(
            name='Email_Distribution_Groups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('GroupName', models.CharField(max_length=100, null=True)),
                ('GroupUsersID', models.CharField(max_length=100, null=True)),
                ('Status', models.BooleanField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Email_Distribution_Groups',
            },
        ),
        migrations.CreateModel(
            name='items_to_mill_mapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField(max_length=200, null=True)),
                ('mill', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'items_to_mill_mapping',
            },
        ),
        migrations.CreateModel(
            name='mill_name_mapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Unit_Name', models.TextField(max_length=500, null=True)),
                ('Mill', models.TextField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Other_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('delivery_Schedule', models.CharField(max_length=100, null=True)),
                ('payment_term', models.CharField(max_length=100, null=True)),
                ('price', models.CharField(max_length=100, null=True)),
                ('matching_source', models.CharField(max_length=100, null=True)),
                ('buyer', models.CharField(max_length=100, null=True)),
                ('any_other_specification', models.CharField(max_length=100, null=True)),
                ('specification_if_no_product_type', models.CharField(max_length=100, null=True)),
                ('commision', models.CharField(max_length=100, null=True)),
                ('Baby_cone', models.BooleanField(max_length=10, null=True)),
                ('air', models.BooleanField(max_length=10, null=True)),
                ('Quantity_type', models.CharField(max_length=200, null=True)),
                ('Reg_no', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'Other_Details',
            },
        ),
        migrations.CreateModel(
            name='purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pono', models.CharField(max_length=200, null=True)),
                ('popdf', models.FileField(max_length=500, null=True, upload_to='')),
            ],
            options={
                'db_table': 'purchase_details',
            },
        ),
        migrations.CreateModel(
            name='Quantity_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feeder_stripes', models.CharField(max_length=100, null=True)),
                ('jacaquard', models.CharField(max_length=100, null=True)),
                ('mini_jaq', models.CharField(max_length=10, null=True)),
                ('auto_stripes', models.CharField(max_length=100, null=True)),
                ('single_jersey', models.CharField(max_length=100, null=True)),
                ('p_k', models.CharField(max_length=10, null=True)),
                ('interlock', models.CharField(max_length=100, null=True)),
                ('rib', models.CharField(max_length=100, null=True)),
                ('white', models.CharField(max_length=10, null=True)),
                ('light', models.CharField(max_length=100, null=True)),
                ('medium', models.CharField(max_length=100, null=True)),
                ('dark', models.CharField(max_length=10, null=True)),
                ('OverDyed', models.CharField(max_length=100, null=True)),
                ('White1', models.CharField(max_length=10, null=True)),
                ('Light1', models.CharField(max_length=100, null=True)),
                ('Dark1', models.CharField(max_length=10, null=True)),
                ('pay_mode', models.CharField(max_length=100, null=True)),
                ('price', models.CharField(max_length=100, null=True)),
                ('number', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(max_length=100, null=True)),
                ('bank', models.CharField(max_length=100, null=True)),
                ('Reg_no', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'Quantity_Details',
            },
        ),
        migrations.CreateModel(
            name='RY_Enquiry_Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reg_no', models.TextField(max_length=200, null=True)),
                ('Mill', models.TextField(max_length=200, null=True)),
                ('Mill_Rep', models.TextField(max_length=200, null=True)),
                ('Customer', models.TextField(max_length=200, null=True)),
                ('Marketing_Zone', models.TextField(max_length=200, null=True)),
                ('Payment_Term', models.TextField(max_length=200, null=True)),
                ('Narration', models.TextField(max_length=200, null=True)),
                ('Reason_For_Non_Acception', models.TextField(max_length=200, null=True)),
                ('Replied_From_the_mill', models.TextField(max_length=200, null=True)),
                ('Acceptance_from_the_mill', models.TextField(max_length=200, null=True)),
                ('Date', models.TextField(max_length=200, null=True)),
                ('Email_Details', models.TextField(max_length=200, null=True)),
                ('Status', models.TextField(max_length=200, null=True)),
                ('CreatedByUser', models.TextField(max_length=200, null=True)),
                ('LastUpdateby', models.TextField(max_length=200, null=True)),
                ('LastUpdateddate', models.TextField(max_length=200, null=True)),
                ('Po_Number', models.CharField(max_length=100, null=True)),
                ('Po_Date', models.CharField(max_length=100, null=True)),
                ('Po_PDF', models.FileField(max_length=500, null=True, upload_to='')),
                ('Po_RevDate', models.CharField(max_length=100, null=True)),
                ('GrpAssignedTo', models.CharField(max_length=100, null=True)),
                ('Sc_Number', models.CharField(max_length=100, null=True)),
                ('Pc_Number', models.CharField(max_length=100, null=True)),
                ('Cop_number', models.CharField(max_length=100, null=True)),
                ('Quotation_Number', models.CharField(max_length=100, null=True)),
                ('Quotation_Date', models.CharField(max_length=50, null=True)),
                ('Ready_stock', models.CharField(max_length=50, null=True)),
                ('Delivery_Date', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'RY_Enquiry_Header',
                'ordering': ['Reg_no'],
            },
        ),
        migrations.CreateModel(
            name='RY_Enquiry_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Counts', models.TextField(max_length=200, null=True)),
                ('Quality', models.TextField(max_length=200, null=True)),
                ('Type', models.TextField(max_length=200, null=True)),
                ('Blend', models.TextField(max_length=200, null=True)),
                ('Shade', models.TextField(max_length=200, null=True)),
                ('Shade_Ref', models.TextField(max_length=200, null=True)),
                ('Depth', models.TextField(max_length=200, null=True)),
                ('UOM', models.TextField(max_length=200, null=True)),
                ('Quantity', models.TextField(max_length=200, null=True)),
                ('Status', models.TextField(max_length=200, null=True)),
                ('Reg_no', models.TextField(max_length=200, null=True)),
                ('Supplier_Rate', models.ImageField(max_length=200, null=True, upload_to='')),
                ('Supplier_Amount', models.ImageField(max_length=200, null=True, upload_to='')),
                ('Supplier_Last_order', models.TextField(max_length=200, null=True)),
                ('Agent_Rate', models.ImageField(max_length=200, null=True, upload_to='')),
                ('Agent_Amount', models.ImageField(max_length=200, null=True, upload_to='')),
                ('Agent_Last_order', models.TextField(max_length=200, null=True)),
                ('CreatedByUser', models.TextField(max_length=200, null=True)),
                ('LastUpdateby', models.TextField(max_length=200, null=True)),
                ('LastUpdateddate', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'RY_Enquiry_Items',
                'ordering': ['Reg_no'],
            },
        ),
        migrations.CreateModel(
            name='ShadeRef_With_mill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shade_ref', models.TextField(max_length=200, null=True)),
                ('shade', models.TextField(max_length=200, null=True)),
                ('type', models.TextField(max_length=200, null=True)),
                ('mill', models.TextField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'ShadeRef_With_mill',
            },
        ),
        migrations.CreateModel(
            name='Upload_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Upload_file', models.FileField(max_length=5000, null=True, upload_to='')),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Upload_by', models.CharField(max_length=100, null=True)),
                ('Upload_Status', models.CharField(max_length=2, null=True)),
                ('Process_Status', models.CharField(max_length=2, null=True)),
            ],
            options={
                'db_table': 'Upload_data',
            },
        ),
        migrations.CreateModel(
            name='User_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('UserName', models.TextField(max_length=200, null=True)),
                ('Password', models.TextField(max_length=200, null=True)),
                ('Role', models.TextField(max_length=200, null=True)),
                ('Status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'User_Details',
                'ordering': ['Role'],
            },
        ),
        migrations.CreateModel(
            name='User_Role_Action',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Role', models.CharField(max_length=10, null=True)),
                ('Status', models.CharField(max_length=10, null=True)),
                ('Action', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'User_Role_Action',
            },
        ),
    ]
