import pandas as pd


class ExcelUtlis:

    excelFileName = ''
    tableame = ''
    df = None

    def __init__(self, excelFileName):
        global df
        df = pd.read_excel(excelFileName)

    def getAllColumns(self):
        return list(df.columns)

    def getAllColumnsAsString(self):
        columnHeader = list(df.columns)
        fullcolStr = ''
        for colName in columnHeader:
            fullcolStr += colName+","
        fullcolStr = fullcolStr[:-1]
        return fullcolStr

    def GenerateDispatchExcelQuery(self, in_excelFileName):

        global getAllColumns

        global excelFileName
        excelFileName = in_excelFileName

        ls = []
        colName = self.getAllColumns()

        for i, row in df.iterrows():

            valuesQueryStr = ''
            for colkey in colName:
                # create a list representing the dataframe row

                # self.getAllColumnsAsString()+") VALUES("
                #print(colkey+" = ", row[colkey])
                if (str(row[colkey]) != None and str(row[colkey]) != 'nan' and str(row[colkey]) != 'NaT'):
                    inserQuery = "INSERT INTO Dispatch_Excel_Dump (Link_ID,DataKey,DataValue) VALUES("
                    inserQuery += "'1','"+colkey + \
                        "','"+str(row[colkey])+"');"

                    ls.append(inserQuery)
        return ls
