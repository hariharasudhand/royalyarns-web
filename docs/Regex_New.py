import re
import string

COUNT_PATTERN = r'\d?\/?\d+[s|S]'
BLEND_PATTERN = r'\d+%'
SHADE_REF_PATTERN = r'^[A-Za-z0-9-]*$'

vCountCheck = False
vBlendCheck = False

##
# THIS HAS TO BE SET IN ROCKET BOT
##
vSHADEColumnNames = {vShade_Col_names}
vQUANTITYColumnNames = {vQuality_Col_Names}
vData = {}

iQtyColumnIndex = -1
iShadeColumnIndex = -1
iAddedIndex = []

# Variable to parse
mailArr = {Mails}
# This method find the index of the column Name
# with the possible match patterns and gets the column Index
# pass Alpha Numerc for Shade Reference this function is used only
# for Shade Ref and Quantity
# def findColumnIndex(emailColumnNameArr, vColMatchStringArr, emailColumnValuesArr, isAlpNumSpecial):
# print("findcolumnname emailColumnValuesArr ", emailColumnValuesArr)
#    colIndex = 0
#    for emailColName in emailColumnNameArr:
#        for colMatchString in vColMatchStringArr:
#            temColMatch = colMatchString.replace(" ", "")
#            temColMatch = temColMatch.lower()
# Check if ColumnNames in Email matches with
# PRe-defined Name Pattern,both strings
# converted to lowercase and spaces removed
#            tempColName = emailColName.replace(" ", "")
#            tempColName = tempColName.lower()
# print(" does --- Column Name Match ",
#      tempColName+" with "+temColMatch)
#            if (tempColName == temColMatch) or (tempColName in temColMatch):

#                if((isAlpNumSpecial) and bool(re.search(SHADE_REF_PATTERN, emailColumnValuesArr[colIndex]))):
#                    return colIndex
#                if((isAlpNumSpecial == False) and (emailColumnValuesArr[colIndex].isdigit())):
#                    return colIndex
#        colIndex = colIndex + 1
#    return -1


def addKeyValue(toKey, value1):

    global vData, convertToArray
    tempData = []
    # print(toKey+" vData ===", vData.get(toKey))
    if (vData.get(toKey) != None):
        tempData = convertToArray(vData.get(toKey))

    if isinstance(value1, list):
        for strvalue in value1:
            tempData.append(strvalue)
    else:
        tempData.append(value1)

    vData[toKey] = None
    vData[toKey] = tempData
    #    return vData


def convertToArray(value):
    if not isinstance(value, list):
        value = [value]
    return value


def checkUnwantedColumn(itemData):
    # print("itemData",itemData)
    isUnwanted = False
    newItem = ""
    for item in itemData:
        if(item != None):
            item = item.replace(' ', '')
            newItem = str(item.lower())
            # print("newItem", newItem)
            if("total" == newItem):
                return True
    return isUnwanted


# First Row will always be the Column Header,mailArr
# contains the whole email value in table as two dimensional array
header = mailArr[0]

counter = 0
for item in mailArr:
    # we assume the first row is always the column names , hence ignoreing that

    if(counter > 0 and checkUnwantedColumn(item) == False):

        # print(" Processing Item ---------------------------------- ", item)
        # FIND SHADE REFERENCE
        # iShadeColumnIndex = findColumnIndex(
        #    mailArr[0], vSHADEColumnNames, item, True)
        # print("iShadeColumnIndex  ", iShadeColumnIndex)
        # if(iShadeColumnIndex >= 0):
        #    print(" Shade Reference  = ", item[iShadeColumnIndex])
        #    addKeyValue(header[iShadeColumnIndex], item[iShadeColumnIndex])

        # AND QUANTITY
        # iQtyColumnIndex = findColumnIndex(
        #    mailArr[0], vQUANTITYColumnNames, item, False)
        # print("iQtyColumnIndex", iQtyColumnIndex)
        # if(iQtyColumnIndex >= 0):
        # print("Quantity =", item[iQtyColumnIndex])
        #    addKeyValue(header[iQtyColumnIndex], item[iQtyColumnIndex])

        # LOOP THROUGH COLUMNS
        columnIndex = 0
        for columnItem in item:

            # CONSIDER ONLY THOSE COLUMNS THAT ARE NOT SHADE REFERENCE OR QUANTITY

            # print("------------------------- checking ",
            #      columnItem+" at index "+str(columnIndex))
            # CHECK FOR COUNT , COUNT AND BLEND ( SOMETIMES COUNT AND BLEND ARE PROVIDED TOGETHER)
            # *--------------------------------------------------------------------------------------------------
            # *
            # * NOW Check if Count and Blend exist together?
            # * it can happen that they are provided seperately as well
            # * --------------------------------------------------------------------------------------------------
            vCountCheck = bool(re.search(COUNT_PATTERN, columnItem))
            # print("["+str(columnIndex) + " ] Checking Regex pattern : " + COUNT_PATTERN + " in " +
            #      columnItem+":" + str(vCountCheck) + "---------------------- column item : ", columnItem)

            if vCountCheck == True:
                vCount = re.findall(COUNT_PATTERN, columnItem)
                print(" vCount = ", vCount[0])

                addKeyValue("COUNT", vCount[0])
                iAddedIndex.append(columnIndex)
                vBlendCheck = bool(re.search(BLEND_PATTERN, columnItem))
                if(vBlendCheck == True):
                    vBlend = columnItem.replace(vCount[0], '')
                    addKeyValue("BLEND", vBlend)
                    # print(" vBlend = ",vBlend)

            # CHECK FOR BLEND
            # check if Blend Global flag is true, this means count and blend are provided
            # together and has been extracted above
            # This will go inside False only if Blend is not found above
            elif(vBlendCheck == False):
                vBlendCheck = bool(re.search(BLEND_PATTERN, columnItem))
                if (vBlendCheck == True):
                    vBlend = columnItem
                    # print(" vBlend ( Seperate Column ) =  ", vBlend)
                    iAddedIndex.append(columnIndex)
                    addKeyValue(header[columnIndex], vBlend)
            columnIndex = columnIndex + 1

        columnIndex = 0
        for columnItem in item:
            if columnIndex not in iAddedIndex:
                # print(" add key value in else : ",
                #      header[columnIndex]+" = "+columnItem+" columnIndex = "+str(columnIndex))
                addKeyValue(header[columnIndex], columnItem)
                # print("************************************************* end checking ",
                #      columnItem+" at index "+str(columnIndex))
            columnIndex = columnIndex + 1
    # Email Row Counter
    counter = counter + 1


print("email content parsed : ", vData)
SetVar('Mail_Parse_Output', vData)
