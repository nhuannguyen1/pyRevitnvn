__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Rename Type Name'
import re
from Autodesk.Revit.DB import Transaction 
from pyrevitnvn import (
                        retr_ele_from_pick,
                        retr_eletype_from_ele,
                        )
from pyrevitnvn.string import typename_from_data
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

#Retrieve element type from pick 1
ele = retr_ele_from_pick()

eleTypeId1 = retr_eletype_from_ele(ele)

string = "Tw_Column_Rafter_WFxW_T2xTmm"

FamilyNameType = typename_from_data(instr=string,
                                    ele=eleTypeId1)

t = Transaction (doc,"Rename Type Name")

t.Start()

SymNew = eleTypeId1.Duplicate(FamilyNameType) 

ele.Symbol = SymNew

t.Commit()
