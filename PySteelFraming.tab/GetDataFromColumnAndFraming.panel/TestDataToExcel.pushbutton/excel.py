# coding: utf8
import clr
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from Microsoft.Office.Interop.Excel import XlListObjectSourceType, Worksheet, Range, XlYesNoGuess
from System.Runtime.InteropServices import Marshal
import os.path
class ExcelApp:
    def __init__(self, app=None, workbook=None):
        self.app = app
        self.workbook = workbook
def initialise():
    """Get active Excel.Application COM object if available or create a new one"""
    # If Excel is open, get it
    try:
        return Marshal.GetActiveObject("Excel.Application")
    # Else open it
    except EnvironmentError:
        return Excel.ApplicationClass()

def release(com_object):
    """Release given Excel.Application COM Object"""
    Marshal.ReleaseComObject(com_object)
def table_style(worksheet, xl_range):
    """
    Apply TableStyle to given Range on given Worksheet
    :type xl_range: Range
    :type worksheet: Worksheet
    """
    worksheet.ListObjects.Add(SourceType=XlListObjectSourceType.xlSrcRange,
                              Source=xl_range,
                              XlListObjectHasHeaders=XlYesNoGuess.xlYes,
                              TableStyleName="TableStyleMedium15")
def workbook_by_name(app, name):
    for workbook in app.Workbooks:
        if workbook.Name == name:
            return workbook
def none():
    try:
        workbook = app.ActiveWorkbook
    except AttributeError:
        workbook = app.Workbooks.Add()
def worksheet_by_name(workbook, name):
    for worksheet in workbook.Sheets:
        if worksheet.Name == name:
            return worksheet
#ex = initialise()
#ex.Visible = True
class DataExcel:
    def  __init__(self, workbook,SheetName):
        self.workbook = workbook
        self.SheetName = SheetName
    def ReturnSheet (self):
        sheet = self.workbook.Sheets(self.SheetName)	
        return sheet
    def FindLastRowOFData (self):
        #workbook = ex.Workbooks.Open(self.path)
        sheet = self.workbook.Sheets(self.SheetName)
        #sheet = self.ReturnSheet()
        i = 1
        while True:
            if (sheet.Cells(i, 1).Value2 == None):
                break 
            i +=1
        return  i -2
    def FindLastColumnOFData (self):
        sheet = self.workbook.Sheets(self.SheetName)
        i = 1
        while True:
            if (sheet.Cells(2, i).Value2 == None):
                break 
            i +=1 
        return  i - 1
    def ArrFistForDefautValue(self):
        col = self.FindLastColumnOFData() 
        ArrDataExcell = []
        for i in range (0,col):
            ArrDataExcell.append(None)
            i +=1
        return ArrDataExcell
    def SaveAsFileExcelReturnSheet(self,path):
        ex = initialise()
        if os.path.isfile(path):
            self.workbook.Close (True)
            workbook = ex.Workbooks.Open(path)
            self.workbook = workbook
            #workbook.Close(False)
            #os.remove(path)
            #self.workbook.SaveAs(path)
            #self.workbook.Save()	                                                                                   
            #workbook = self.Workbook.Open(path)
            sheet = workbook.Sheets(self.SheetName)
            print ("sheet is path ",sheet)
            workbook.Save()
            
        else:
            workbook = ex.ActiveWorkbook
            workbook.SaveAs(path)
            #self.workbook.Close(False)
            #workbook = self.workbook.Open(path)
            sheet = workbook.Sheets(self.SheetName)
            print ("sheet is sheet ",sheet)
            workbook.Save()
        return sheet