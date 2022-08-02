import pandas as pd

class ExcelUtlis:

    excelFileName = ''
    tableame = ''
    df = None


    def init():
        global df
        df = pd.read_excel(excelFileName)


    def setExcelFileName(in_excelFileName):
        global excelFileName
        excelFileName = in_excelFileName


    def setTableName(in_Tableame):
        global tableame
        tableame = in_Tableame


    def getAllColumns():
        return list(df.columns)


    def getAllColumnsAsString():
        columnHeader = list(df.columns)
        fullcolStr = ''
        for colName in columnHeader:
            fullcolStr += colName+","
            fullcolStr = fullcolStr[:-1]
        return fullcolStr


    def GetInsertQueryList(in_excelFileName):
        global setExcelFileName, init, getAllColumns, getAllColumnsAsString
        setExcelFileName(in_excelFileName)
        init()
        ls = []
        colName = getAllColumns()
        # iterate over the rows
        inserQuery = "INSERT INTO TABLENAME ("+getAllColumnsAsString()+") VALUES("
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


    # print(getAllColumnsAsString())
    print(GetInsertQueryList(
    'D:\work\royalyarns-web\media'))