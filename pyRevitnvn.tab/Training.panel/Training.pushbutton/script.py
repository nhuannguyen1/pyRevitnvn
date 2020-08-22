__doc__ = 'Create gird by parameter from excel file'
__author__ = 'Nguyen Van Nhuan - pyan.vn'
__title__ = 'DGrid'
import xlrd,os
from Autodesk.Revit.DB import Transaction
from pyrevitnvn.draw.gird import dgrid
from pyrevitnvn.draw import draw

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# retrieve active view 
view = doc.ActiveView

# retrieve dir path from abspath 
dir_path = os.path.dirname(os.path.abspath(__file__))

# retrieve fullname excel file 
file_loc =os.path.join(dir_path,"Create_Grids.xlsx")

# open wb by xlrd 
workbook = xlrd.open_workbook(filename=file_loc)
# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)