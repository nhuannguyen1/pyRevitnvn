from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import forms
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