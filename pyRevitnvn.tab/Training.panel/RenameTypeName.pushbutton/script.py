__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Rename Type Name'
import re
from Autodesk.Revit.DB import Transaction 
from pyrevitnvn.units import Convert_From_Internal_Display_Length
from pyrevitnvn import retr_ele_from_pick,retr_eletype_from_ele,typename_from_data

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def get_parameter_value_by_name(element, parameterName):
    return element.LookupParameter(parameterName).AsString()

def set_parameter_by_name(element, parameterName, value):
   return element.LookupParameter(parameterName).Set(value)

def dictfrompara(ele,
                 para_names
                 ):
    return {para_name :Convert_From_Internal_Display_Length(ele.LookupParameter(para_name).AsDouble()) for para_name in para_names}

def typename_from_data(instr = "",
                 ele = None,
                 pattern = 'x|mm'
                 ):

    listparam = list(filter(lambda x: x !="",re.split(pattern, instr)))

    dictele = dictfrompara(ele=ele,
                           para_names=listparam
                           ) 

    for param_name in listparam:

        instr = instr.replace(param_name,str(dictele[param_name]))

    return instr

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
