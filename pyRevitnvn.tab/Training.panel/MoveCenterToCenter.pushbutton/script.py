from Autodesk.Revit.DB import Transaction
__doc__ = "Move Center To Center"
__title__ = "CTC"
__author__ = "pyan.vn"
from pyrevitnvn import retr_loc_ele_from_pick
from pyrevitnvn import forms
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Retrieve loction of move object 
locp_m = retr_loc_ele_from_pick()

if type(locp_m).__name__ != "LocationPoint":
    forms.alert("This type of object is not LocationPoint")

# Retrieve loction of not_move object 
locp_nm = retr_loc_ele_from_pick()

if type(locp_nm).__name__ != "LocationPoint":
    forms.alert("This type of object is not LocationPoint")

# retrieve point of not_move object 
point_nm = locp_nm.Point

# star transaction 
t = Transaction (doc,"Move center to center other object")
t.Start()

# set point new for location object move 
locp_m.Point = point_nm

# commit transaction 
t.Commit()