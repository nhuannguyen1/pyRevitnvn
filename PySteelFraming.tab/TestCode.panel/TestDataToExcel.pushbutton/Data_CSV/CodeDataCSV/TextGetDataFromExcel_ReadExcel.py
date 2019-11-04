import pandas as pd
from pandas import ExcelWriter,ExcelFile
import numpy as np
import csv
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from Path_Connect_Excel import Right_Genneral_All_path,Left_Genneral_All_path,DataExcel,Config_Setting_Path
#from Csv_Connect_Data import ReturnDataAllRowByIndexpath
NewExcel = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\CodeDataCSV\new_big_file.xlsx'
xxx = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\xxx.csv'
book = load_workbook(DataExcel)
#book.template = True
#import xlwings as xw
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
def GetIndexOfNotChange(IndexChange,IndexChangeTotal):
    IndexArr =  [IndexChangeTotal.index(indexc) for indexc in IndexChange]
    return  IndexArr
def AligntText(sheet):
    rows = range(1, 44)
    columns = range(1, 44)
    for row in rows:
        for col in columns:
            sheet.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)    
def CreateFileCSV():
    df = pd.read_excel(NewExcel,'Right Member',index_col= 0)
    df.to_csv(xxx,index=True)
CreateFileCSV() 