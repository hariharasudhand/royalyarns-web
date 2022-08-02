from .models import Upload_Data
from .dispatch_model import Dispatch_Header, Dispatch_Excel_Dump

import pandas as pd


class DispatchDAO:

    name = ''

    def __init__(self, name):
        self.name = name
    #
    # Store  Dispatch_Header and Dispatch_Excel_Dump
    #

    def StoreUpload_Data(self, vExcelPath, vDate, vUser):

        vExcelFileURL = "/Users/harid/work/weeroda/RoyalYarns/teratta-app/media/"+vExcelPath.name
        print('Processing Upload Excel File Name : ', vExcelFileURL)
        ls = []
        vQueryResult = Upload_Data.objects.create(
            Upload_file=vExcelPath, Date=vDate, Upload_by=vUser, Upload_Status='1', Process_Status='0'
        )
        print(str(vQueryResult))
        if vQueryResult != None:
            print("vQueryResult", vQueryResult.id)
            # ***** Now that the Upload is Sucessful, we can proceed *****

            ##
            # LOAD UPLOAED EXCEL FILE , read rows and cells and insert into
            # Dispatch_Header Table and Dispatch_Excel_Dump
            ##
            vExcelWorkbook = pd.ExcelFile(vExcelFileURL)

            for sheetName in vExcelWorkbook.sheet_names:
                print("******* Processing Sheet Name : ", sheetName)
                # 1: Lets insert into Dispatch_Header Table
                vQueryDHResult = Dispatch_Header.objects.create(
                    Link_ID=str(vQueryResult.id), Excel_Sheet_Name=sheetName)

                df = pd.read_excel(vExcelFileURL, sheet_name=sheetName)

                # get ColumnNames
                colNameList = list(df.columns)
                # ITERATE EACH ROWS
                for i, row in df.iterrows():
                    for colkey in colNameList:
                        if (str(row[colkey]) != None and str(row[colkey]) != 'nan' and str(row[colkey]) != 'NaT'):
                            Dispatch_Excel_Dump.objects.create(
                                Link_ID=str(vQueryResult.id), Link_Header_ID=str(vQueryDHResult.id), DataKey=colkey, DataValue=str(row[colkey]))
