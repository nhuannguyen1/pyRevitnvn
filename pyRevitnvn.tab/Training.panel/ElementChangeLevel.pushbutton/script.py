__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Test Code'
# Import commom language runtime
import xlrd
import string
# Import commom language runtime
# Import Revit API
from Autodesk.Revit.DB import *
                        
from Autodesk.Revit.UI.Selection.Selection import PickObjects
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import TaskDialog,TaskDialogCommonButtons,TaskDialogResult 
# doc
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
def col2num(col):
    """
    Return number corresponding to excel-style column \n
    ex: A--->1,B--->2 
    """
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


#cap = doc.GetElement(pick)
# Get data excel
def data(file_loc = r"D:\01. Project\01. Python_Trainning\Pyrevit/python\Category_List.xlsx",name_color = "C", red = "D", green = "E", blue = "F"):
    # Pick Object 
    print ("file_loc",file_loc)
    workbook = xlrd.open_workbook(file_loc)
    sheet = workbook.sheet_by_index(0)
    list_cate = []
    rows = sheet.nrows
    cell_option1 = sheet.cell_value(1,3)
    print(cell_option1)
    # for row in range(rows):
    #     cell = sheet.cell_value(row,col2num(index_col)-1)
    #     if cell != "":
    #         list_cate.append(cell)
    # list_cate = list_cate[1:None]
    
data(file_loc = r"D:\3.Draf\xlrd1.xlsx",name_color = "C", red = "D", green = "E", blue = "F")
