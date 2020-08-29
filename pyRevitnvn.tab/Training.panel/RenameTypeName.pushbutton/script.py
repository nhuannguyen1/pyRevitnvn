__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Rename Type Name'
import re
from Autodesk.Revit.DB import Transaction 
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevitnvn.units import Convert_From_Internal_Display_Length
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
from pyrevitnvn import retr_ele_from_pick,retr_eletype_from_ele

def get_parameter_value_by_name(element, parameterName):
    return element.LookupParameter(parameterName).AsString()

def set_parameter_by_name(element, parameterName, value):
   return element.LookupParameter(parameterName).Set(value)


def dictfrompara(ele,para_names = []):
    return {para_name :Convert_From_Internal_Display_Length(ele.LookupParameter(para_name).AsDouble()) for para_name in para_names}

def changestring(instr,ele):
    pattern = 'x'
    result = re.split(pattern, instr) 
    dictele = dictfrompara(ele=ele,para_names=result)
    for param_name in result:
        instr = instr.replace(param_name,str(dictele[param_name]))
    return instr

#Retrieve element type from pick 1
ele = retr_ele_from_pick()

eleTypeId1 = retr_eletype_from_ele(ele)

string = "Tw_Column_Rafter_WFxW_T2xT"

FamilyNameType = changestring(instr=string,
                              ele=eleTypeId1)

t = Transaction (doc,"Rename Type Name")
t.Start()

SymNew = eleTypeId1.Duplicate(FamilyNameType) 
ele.Symbol = SymNew
t.Commit()
