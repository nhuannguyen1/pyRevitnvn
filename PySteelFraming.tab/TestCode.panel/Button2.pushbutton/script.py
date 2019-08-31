__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Element
from Autodesk.Revit.UI.Selection import  ObjectType 
#Get UIDocument and Document
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
#Pick Object
pick = uidoc.Selection.PickObject(ObjectType.Element)
#retrieve elenment
eleid = pick.ElementId
ele = doc.GetElement(eleid)
# Get paramenter
param = ele.LookupParameter("H_n")
print (ele)
print (param)