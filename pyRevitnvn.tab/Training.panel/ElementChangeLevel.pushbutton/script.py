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

import os

# retrieve dir path from abspath 
dir_path = os.path.dirname(os.path.abspath(__file__))

# retrieve fullname excel file 
file_loc =os.path.join(dir_path,"Category_List.xlsx")

# retrieve workbook 
workbook = xlrd.open_workbook(file_loc)

# retrieve sheet
sheet = workbook.sheet_by_index(0)

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

def pattern_color(name_pattern = "<Solid fill>"):
    """ 
    return pattern of fill lcolor by name 
    """
    patterns = FilteredElementCollector(doc).OfClass(FillPatternElement)

    for pattern in patterns:
        if pattern.Name == name_pattern:
            solidPatternId = pattern.Id
            break
    return solidPatternId

def id_sym(ele):
    """
    convert elementtype to id 
    """

    ele_type = ele.GetTypeId()
    return ele_type.ToString()

def d_from_idsym_ele(fele):
    """ 
    return dict from FilteredElementCollector
    id: key of elementtype
    value: family instace 
    """
    # list key id 
    lkey_ids = set(map(id_sym,fele))
    dicta = {}
    for key_id in lkey_ids:
        dicta[key_id] = [ele for ele in fele if ele.GetTypeId().ToString() == key_id]
    return dicta

def run(col_color_index = "D"):

    # retrieve List color from excel file 
    lcolor = [sheet.cell_value(row,col2num(col_color_index)-1) for row in range(1,sheet.nrows)]
    
    # Filtered Element Collector family instance 
    family_instance = FilteredElementCollector(doc).OfClass(FamilyInstance)

    # start transaction
    t = Transaction(doc, "Override Element")
    t.Start()

    # remove duplicate id 
    lkey_ids = set(map(id_sym,family_instance))

    # create dict key: id, value: family instace
    dic_ele = d_from_idsym_ele(lkey_ids,family_instance)

    for index,keyid in enumerate(lkey_ids):

        # get list family instace 
        ele_ins = dic_ele[keyid]

        # get index of color 
        r,b,g = eval(lcolor[index])

        for ele_in in ele_ins:

            # get color 
            color_ele = Color(r,b,g)
            # Settings to override display of elements in a view.
            override = OverrideGraphicSettings()

            # Sets the projection surface fill color
            override.SetProjectionFillColor(color_ele) 

            # Sets the projection surface fill pattern
            override.SetProjectionFillPatternId(pattern_color())

            # Sets graphic overrides for an element in the view.
            view.SetElementOverrides(ele_in.Id, override)
    
    # commit transaction
    t.Commit()
run(path = file_loc, col_color_index = "A")