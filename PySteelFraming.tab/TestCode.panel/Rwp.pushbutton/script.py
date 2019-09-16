import clr
# import the Excel Interop. 
clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal
import xlrd 
# file path of excel file. 
path = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\Rwp.pushbutton\ExcelTest.xlsx"
# Instantiate the Excel Application
ex = Excel.ApplicationClass()
# Make it Visiable for us all to see
ex.Visible = False
# Disable Alerts - Errors Ignore them, they're probably not important
ex.DisplayAlerts = False
# Workbook 
workbook = ex.Workbooks.Open(path)
# WorkSheet

ws = workbook.Worksheets[1]
# Cell range
print (ws.Rows[1].Value2[0,0])
# close and release excel file from memory. 
ex.ActiveWorkbook.Close(False)
Marshal.ReleaseComObject(ws)
Marshal.ReleaseComObject(workbook)
Marshal.ReleaseComObject(ex)