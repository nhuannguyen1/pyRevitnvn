__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Test Code'
# Import commom language runtime
import xlrd
# Import commom language runtime
# Import Revit API
from Autodesk.Revit.UI.Selection import  ObjectType 
from Autodesk.Revit.Creation.ItemFactoryBase import NewDimension
import os
# Import Revit API
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

def Convert_length(length):
    """ 
    convert  length To Internal Units \n
    Converts a value from a given display unit to Revit's internal units.
    """
    # retrieve unit display current in revit 
    unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
    display_unit = unit_format_options.DisplayUnits
    return UnitUtils.ConvertToInternalUnits(float(length), display_unit)

offsetv = Convert_length(9000)

print (offsetv)
# retrieve dir path from fullname 
dir_path = os.path.dirname(os.path.abspath(__file__))
# retrieve directory excel file 
file_loc =os.path.join(dir_path,"Create_Grids.xlsx")
# open wb by xlrd 
workbook = xlrd.open_workbook(file_loc)
# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)
def LbyRange (sheet = None, index_col = "A", value_ignore = ["",None]):
    """ 
    return list by range excel
    """
    trucX = [cell_value in row in range(rows) if all(sheet.cell_value(row,0) != value_ignore)]

trucX = []
rows = sheet.nrows
for row in range(rows):
    cell = sheet.cell_value(row,0)
    if cell != "":
        trucX.append(cell)
trucX = trucX[1:None]









# ky hieu truc X
trucX = []
rows = sheet.nrows
for row in range(rows):
    cell = sheet.cell_value(row,0)
    if cell != "":
        trucX.append(cell)
trucX = trucX[1:None]

# ky hieu truc Y
trucY = []
rows = sheet.nrows
for row in range(rows):
    cell = sheet.cell_value(row,2)
    if cell != "":
        trucY.append(cell)
trucY = trucY[1:None]

# khaong cach truc X
disX = []
rows = sheet.nrows
for row in range(rows):
    cell = sheet.cell_value(row,1)
    if cell != "":
        disX.append(cell)
disX = disX[1:None]

# khoang cach truc Y
disY = []
rows = sheet.nrows
for row in range(rows):
    cell = sheet.cell_value(row,3)
    if cell != "":
        disY.append(cell)
disY = disY[1:None]

t = Transaction(doc, "Dimension grids")
t.Start()
# ham chuyen don vi mm
def number_mm(mylist):
    "chuyen doi mm"
    mylist1 = UnitUtils.ConvertToInternalUnits(mylist, DisplayUnitType.DUT_MILLIMETERS)
    return(mylist1)
# truc X1
dicta = dict(zip(trucX, disX))
dictb = dict(zip(trucY, disY))
c = 0
v = 0
for i in trucX:
    x1 = dicta.get(i)
    x2 = number_mm(x1)
    c = c + x2
    XYZStart1 = XYZ(c,0,0)
    XYZEnd1 = XYZ(c,offset,0)
    lineCD = Line.CreateBound(XYZStart1, XYZEnd1)
    grid_1 = Grid.Create(doc, lineCD)
    name = grid_1.get_Parameter(BuiltInParameter.DATUM_TEXT)
    name_1 = name.Set(i)
for y in trucY:
    y1 = dictb.get(y)
    y2 = number_mm(y1)
    v = v + y2
    XYZStart2 = XYZ(0,v,0)
    XYZEnd2 = XYZ(offset,v,0)
    line2 = Line.CreateBound(XYZStart2, XYZEnd2)
    grid_2 = Grid.Create(doc, line2)
    namex = grid_2.get_Parameter(BuiltInParameter.DATUM_TEXT)
    name_2 = namex.Set(y)
t.Commit()