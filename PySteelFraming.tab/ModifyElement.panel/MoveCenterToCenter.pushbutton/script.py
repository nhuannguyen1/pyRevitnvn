from Autodesk.Revit.DB import*
from Autodesk.Revit.UI import*
from Autodesk.Revit.Attributes import*
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction, BuiltInParameter, Element, Level, MEPCurve, ElementId, FamilyInstance\
    , FilteredElementCollector
__doc__ = "Change selected elements level without moving it"
__title__ = "MoveCenterToCenter"
__author__ = "Cyril Waechter"

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

pick1 = uidoc.Selection.PickObject(ObjectType.Element)
pick2 = uidoc.Selection.PickObject(ObjectType.Element)
#retrieve elenment 1
eleid1 = pick1.ElementId
ele1 = doc.GetElement(eleid1)
#retrieve elenment 2
eleid2 = pick2.ElementId
ele2 = doc.GetElement(eleid2)
locp1 = ele1.Location
locp2 = ele2.Location
if (pick1 == None) or (pick2 == None):
	print ("Pick firt or pick second not selection ")
else:
    if locp1 != None:
        t = Transaction (doc,"Move center to center other element")
        t.Start()
        Loc = locp1.Point
        Locnew = locp2.Point
        locp1.Point = Locnew
        t.Commit()
    else:
        print ("Location is null")