import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import csv
from openpyxl import load_workbook
#from Csv_Connect_Data import ReturnDataAllRowByIndexpath
Right_Genneral_All_path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\Right_Genneral_All.csv'
Left_Genneral_All_path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\Left_Genneral_All.csv'
Config_Setting_Path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\Config_Setting - Copy.csv'
book = load_workbook(Left_Genneral_All_path)
def ReturnDataAllRowByIndexpath (path,NumberRow):
        with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        RowNumber.pop(0)
        return RowNumber
def HandlingDataSTr (Element):
    Element1 = Element.replace(":",",")
    Element2= Element1.replace("(","")
    Element3= Element2.replace(")","")
    return eval(Element3)
ArrPAth = [Left_Genneral_All_path,Right_Genneral_All_path]
IndexChange = ReturnDataAllRowByIndexpath(Config_Setting_Path,0)
IndexChange =  [int(i) for i in IndexChange]
#IndexGeneral = [11,12,14,15,16]
IndexGeneral = ReturnDataAllRowByIndexpath(Config_Setting_Path,22)
IndexGeneral = [int(i) for i in IndexGeneral]
#remove Column move 
Columnmove = ReturnDataAllRowByIndexpath(Config_Setting_Path,32)
Columnmove = [int(i) for i in Columnmove]
LocationCellForMoveColumn = ReturnDataAllRowByIndexpath(Config_Setting_Path,34)
s1 = set(IndexChange).difference(set(Columnmove))
LeftMember = list(s1)

writer = ExcelWriter('DataALL.xlsx',engine='xlsxwriter')

for path in ArrPAth:
    if path == Left_Genneral_All_path:
        df1 = pd.read_csv(path, delimiter=',',index_col = 0)
        df1.to_csv(path)
        df = pd.read_csv(path, delimiter=',',index_col = None ,usecols = IndexGeneral,nrows= 1 )
        dfChange = pd.read_csv(path, delimiter=',',index_col = None ,usecols = LeftMember )
        df.to_excel(writer,'General Member',index=False)
        dfChange.to_excel(writer,'Left Member',index=False)
        worksheet = writer.sheets['Left Member']
        #Wirte Column to csv
        for cell,index in zip(LocationCellForMoveColumn,Columnmove):
            cellstr = HandlingDataSTr(cell)
            df = pd.read_csv(path, delimiter=',',index_col = None ,usecols = [index],nrows= 1)
            worksheet.write(cellstr[0], cellstr[1],df.iat[0,0]) 
    else:
        df1 = pd.read_csv(path, delimiter=',',index_col = 0)
        df1.to_csv(path)
        dfChange = pd.read_csv(path, delimiter=',',index_col = None ,usecols = LeftMember )
        dfChange.to_excel(writer,'Right Member',index=False)
        worksheet = writer.sheets['Right Member']
        for cell,index in zip(LocationCellForMoveColumn,Columnmove):
            cellstr = HandlingDataSTr(cell)
            df = pd.read_csv(path, delimiter=',',index_col = None ,usecols = [index],nrows= 1)
            print (cellstr[0], cellstr[1])
            worksheet.write(cellstr[0], cellstr[1],df.iat[0,0]) 
writer.save()
