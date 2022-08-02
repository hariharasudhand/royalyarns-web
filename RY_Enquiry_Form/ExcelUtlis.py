import pandas as pd


class ExcelUtlis:

    excelFileName = ''
    tableame = ''
    df = None

    def __init__(self, excelFileName):
        global df
        df = pd.read_excel(excelFileName)

    def setTableName(self, in_Tableame):
        global tableame
        tableame = in_Tableame

    def getAllColumns(self):
        return list(df.columns)

    def getAllColumnsAsString(self,):
        columnHeader = list(df.columns)
        fullcolStr = ''
        for colName in columnHeader:
            fullcolStr += colName+","
            fullcolStr = fullcolStr[:-1]
        return fullcolStr

    def GetInsertQueryList(self, in_excelFileName):

        global getAllColumns, getAllColumnsAsString

        global excelFileName
        excelFileName = in_excelFileName

        ls = []
        colName = getAllColumns()
        # iterate over the rows
        inserQuery = "INSERT INTO TABLENAME (" + \
            getAllColumnsAsString()+") VALUES("
        for i, row in df.iterrows():
            valuesQueryStr = ''
        for colkey in colName:
            # create a list representing the dataframe row

            #print(colkey+" = ", row[colkey])
            if (str(row[colkey]) != None and str(row[colkey]) != 'nan' and str(row[colkey]) != 'NaT'):
                valuesQueryStr += "'"+str(row[colkey])+"'"+","
    # append row list to ls

    # print("valuesQueryStr", valuesQueryStr)
            inserQuery += valuesQueryStr[:-1] + ")"
            ls.append(inserQuery)
            return ls

    # GET COLUMN NAME as STRING with COMMO SEPERATED VALUES

    # vExcelUtlis = ExcelUtlis()
    # # # print(getAllColumnsAsString())
    # print(vExcelUtlis.GetInsertQueryList(
    #     'D:\work\royalyarns-web\media'))
