__doc__ = 'Create gird by parameter from excel file'
__author__ = 'Nguyen Van Nhuan - pyan.vn'
__title__ = 'DGrid'
import xlrd,os
from Autodesk.Revit.DB import Transaction
from pyrevitnvn.draw import draw
from pyrevitnvn.draw.gird import d2grid
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

# retreve value cell from excel, starting coordinates of
# horizontal(ocy) and vertical (ocx)
try: 
    ocx = eval(sheet.cell_value(0,1))
except:
    ocx = None
try:
    ocy = eval(sheet.cell_value(0,4))
except:
    ocy = None

@draw(file_loc)
def run():
    d2grid(ver_name_text_gird_col="A",
           ver_dist_gird_col="B",
           ver_length_gird_col="C",
           ver_coord_start=ocx,
           hor_name_text_gird_col="D",
           hor_dist_gird_col="E",
           hor_length_gird_col="F",
           hor_coord_start=ocy,
           sheet=sheet
            )
run()