__doc__ = 'Create gird by parameter from excel file'
__author__ = 'Nguyen Van Nhuan - pyan.vn'
__title__ = 'DGrid'
import xlrd,os
from Autodesk.Revit.DB import Transaction
from pyrevitnvn.draw import draw
from pyrevitnvn.draw.gird import dgrid,d2grid

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
ocx = eval(sheet.cell_value(0,1))
ocy = eval(sheet.cell_value(0,4))

@draw(file_loc)
def run():
    """ 
    drawing gird by parameter from excel\n
    name_text_gird: 
    name_text_gird: colum index from  excel to retrieve text gird \n
    dist_gird_col: distance of gird \n
    length_gird_col: length of gird \n
    type: horizontal or vertical \n  
          the direction axis \n
          default value: vertical \n
    sheet: worksheet input \n
    coord_start: starting coordinates
    """
    # drawing gird to project revit 
    #dgrid(name_text_gird_col="A",dist_gird_col="B",length_gird_col="C",coord_start=ocx,type_d="vertical",sheet=sheet)
    #dgrid(name_text_gird_col="D",dist_gird_col="E",length_gird_col="F",coord_start=ocy,type_d="horizontal",sheet=sheet)

    d2grid(sheet=sheet,hor_coord_start=ocy,ver_coord_start=ocx)

run()