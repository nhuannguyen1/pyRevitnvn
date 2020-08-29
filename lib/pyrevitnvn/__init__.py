from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import forms
from pyrevitnvn.units import Convert_length
import re
from pyrevitnvn.units import Convert_From_Internal_Display_Length
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
def retr_loc_ele_from_pick():
    """ 
    retrieve loccation element from pick object 
    """
    # pick object on revit project (object move)
    pick_m = uidoc.Selection.PickObject(ObjectType.Element)

    #retrieve id (object move)
    eleid_m = pick_m.ElementId

    #retrieve elenment (object move)
    ele_m = doc.GetElement(eleid_m)

    # check picked or not 
    if pick_m == None:
        # alert error 
	    forms.alert("Not Yet Pick Object")
    
    return ele_m.Location

def retr_ele_from_pick():
    """ 
    retrieve element from pick object 
    """
    # pick object on revit project 
    pick = uidoc.Selection.PickObject(ObjectType.Element)

    # check pick
    if pick == None:
	    forms.alert("Not Yet Pick Object")

    #retrieve id element
    eleid_m = pick.ElementId

    return doc.GetElement(eleid_m)


def retr_eletype_from_ele(ele):
    """ 
    retrieve element from ele 

    """
    return doc.GetElement(ele.GetTypeId()) 

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