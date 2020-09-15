from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import forms
from pyrevitnvn.units import Convert_length
from Autodesk.Revit.DB import Element,FilteredElementCollector,FillPatternElement 
import re
from pyrevitnvn.units import Convert_From_Internal_Display_Length
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
import string
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


def ltype_name_in_Family(eletype):
    """
    return list type name 
    """
    family = eletype.Family
    return [Element.Name.__get__(doc.GetElement(symid)) for symid in family.GetFamilySymbolIds()]

def familysymbol_by_name(eletype,name_type):
    """
    Get familysymbol by name 
    """

    # Retrieve family from ele type
    family = eletype.Family
    for familysymbol in family.GetFamilySymbolIds():
        # Get symbol type name 
        FamilySymbolName = Element.Name.__get__(doc.GetElement(familysymbol))
        if FamilySymbolName == name_type:
            return familysymbol
            break


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

def dict_by_familyinstance(fele):
    """ 
    return dict from FilteredElementCollector
    id: key of elementtype
    value: family instace 
    """
    # remove duplicate id 
    lkey_ids = set(map(id_sym,fele))
    dicta = {}
    for key_id in lkey_ids:
        dicta[key_id] = [ele for ele in fele if ele.GetTypeId().ToString() == key_id]
    return dicta