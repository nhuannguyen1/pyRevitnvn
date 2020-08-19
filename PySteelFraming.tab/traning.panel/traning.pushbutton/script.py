__doc__ = 'Create gird by parameter from excel file'
__author__ = 'Nguyen Van Nhuan'
__title__ = 'DGrid'
import xlrd
import os
from Autodesk.Revit.DB import Transaction
from pyrevitnvn.draw.gird import dgird
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
# retrieve dir path from fullname 
dir_path = os.path.dirname(os.path.abspath(__file__))
# retrieve directory excel file 
file_loc =os.path.join(dir_path,"Create_Grids.xlsx")
# open wb by xlrd 
workbook = xlrd.open_workbook(filename=file_loc)
# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)
t = Transaction(doc, "Create grids")
# retreve value cell from excel
Origin_Coordx = eval(sheet.cell_value(0,1))
Origin_Coordy = eval(sheet.cell_value(0,4))
t.Start()
# drawing gird by parameter from excel 
dgird(name_text_gird="D",
        dist_gird_col="E",
        length_gird_col="F",
        type="horizontal",
        coord_start=Origin_Coordy,
        sheet=sheet
        )
dgird(name_text_gird="A",
        dist_gird_col="B",
        length_gird_col="C",
        coord_start=Origin_Coordx,
        sheet=sheet
        )
t.Commit()
