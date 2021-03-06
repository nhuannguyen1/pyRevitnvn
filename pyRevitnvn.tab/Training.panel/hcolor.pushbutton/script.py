__doc__ = 'Change color of element solid with index color from excel file '
__author__ = 'nguyenvannhuan90123@gmail.com - pyan.vn'
__title__ = 'orcolor'

from Autodesk.Revit.DB import (FilteredElementCollector,
                               FamilyInstance,
                               Transaction,Color,
                               OverrideGraphicSettings
                               )
from pyrevitnvn import (dict_by_familyinstance,
                        pattern_color
                        )
from pyrevitnvn.draw import draw
from pyrevitnvn.pyan_string import col2num,eval_str

import os,xlrd

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

# retrieve dir path from abspath 
dir_path = os.path.dirname(os.path.abspath(__file__))

# retrieve fullname excel file 
file_loc =os.path.join(dir_path,"lcolor.xlsx")

# retrieve workbook 
workbook = xlrd.open_workbook(file_loc)

# retrieve sheet
sheet = workbook.sheet_by_index(0)

@draw(file_loc)
def run():

    # retrieve List color from excel file 
    lcolor = [sheet.cell_value(row,col2num("A")-1) for row in range(1,sheet.nrows)]

    # eval ele in list
    lcolor = map(eval_str,lcolor)

    # Filtered Element Collector family instance 
    f_family_ins = FilteredElementCollector(doc).OfClass(FamilyInstance)
    
    # create dict key: id, value: family instaces
    dic_ele = dict_by_familyinstance(f_family_ins)

    # start index value 
    index = 0

    # start transaction
    t = Transaction(doc, "Change Color Element")
    t.Start()

    for keyid in list(dic_ele.keys()):

        if index >= len(lcolor):
            index = 0
        
        # get index of color 
        r,b,g = lcolor[index]

        # get color
        color_ele = Color(r,b,g)

        for ele_in in dic_ele[keyid]:
            # Settings to override display of elements in a view.
            override = OverrideGraphicSettings()

            # Sets the projection surface fill color
            override.SetProjectionFillColor(color_ele) 

            # Sets the projection surface fill pattern
            override.SetProjectionFillPatternId(pattern_color())

            # Sets graphic overrides for an element in the view.
            view.SetElementOverrides(ele_in.Id, override)
            
        index = index + 1
    # commit transaction
    t.Commit() 

    
run()