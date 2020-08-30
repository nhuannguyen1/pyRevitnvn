__doc__ = 'Rename type name of family, type name retrieve from itself parameter'
__author__ = 'pyan.vn'
__title__ = 'Rename Type Name'
import os
import re
import xlrd
from Autodesk.Revit.DB import Transaction 
from pyrevitnvn import (
                        retr_ele_from_pick,
                        retr_eletype_from_ele,
                        familysymbol_by_name
                        )
from pyrevitnvn.string import typename_from_data,pattern_by_user
from pyrevitnvn import ltype_name_in_Family
from pyrevitnvn.draw import draw

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
# retrieve dir path from abspath 
dir_path = os.path.dirname(os.path.abspath(__file__))

# retrieve fullname excel file 
file_loc =os.path.join(dir_path,"infor.xlsx")

# open wb by xlrd 
workbook = xlrd.open_workbook(filename=file_loc)

# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)

# retrieve value of B1
type_name_format = sheet.cell_value(0,1)

# retrieve value of B2
pattern = sheet.cell_value(1,1)

@draw(file_loc)
def run():

    #Retrieve element type from pick
    ele = retr_ele_from_pick()

    # retrieve element type from element
    eletype = retr_eletype_from_ele(ele)

    # Get name  of type family 
    new_name_type = typename_from_data(instr=type_name_format,
                                       ele=eletype,
                                       pattern=pattern
                                       )

    #Start transaction 
    t = Transaction (doc,"Rename Type Name Of Family ")
    t.Start()

    # return list type name in family 
    all_name_types = ltype_name_in_Family(eletype)
    
    # check if type name is existing, get current type name 
    if new_name_type in all_name_types:

        # Retrieve familysymbol by type name
        familysymbol = familysymbol_by_name(eletype=eletype,
                                            name_type=new_name_type
                                            )
        
        # Retrieve element of familysymbol 
        symbol = doc.GetElement(familysymbol)

    else:

        # duplicate tye with  type name has been change 
        symbol = eletype.Duplicate(new_name_type)

    # Returns or changes the FamilySymbol object that represents the type of the instance.
    ele.Symbol = symbol

    # commit transaction
    t.Commit()

run()