# coding: utf8

__doc__ = """Create sections from selected linear objects (eg. walls)
SHIFT-CLICK to display options"""
__title__ = "CreateSectionFrom"
__author__ = "Cyril Waechter"

from Autodesk.Revit.DB import Document, Line, FilteredElementCollector, ViewFamilyType, ViewFamily, Element, \
    ViewSection, Transform, BoundingBoxXYZ, XYZ, BuiltInParameter,Transaction
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit import Exceptions
from Autodesk.Revit.UI.Selection import *
from pyrevit import script, forms
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
collectors = FilteredElementCollector(doc).OfClass(ViewFamilyType)
t = Transaction(doc, 'This is my new transaction')
t.Start()
# Select an element in Revit
picked = uidoc.Selection.PickObject(ObjectType.Element, "Select something.")
eleid = picked.ElementId
ele = doc.GetElement(eleid)
# Get bounding box of selected element.
#picked_bb = BoundingBoxXYZ()
picked_bb = ele.get_BoundingBox(doc.ActiveView)  
# Get max and min points of bounding box.
picked_bb_max = picked_bb.Max
picked_bb_min = picked_bb.Min
print (picked_bb_max)
print (picked_bb_min)
for collector in collectors:
    tn = Element.Name.__get__(collector)
    if tn == 'IIa.Detail Anchor Bolt':
        ViewFamilyTypeId = collector.Id     
Point1 = XYZ(picked_bb_min.X,picked_bb_min.Y,0)
Point2 = XYZ(picked_bb_max.X,picked_bb_max.Y,0)
ViewParent = doc.ActiveView
ViewParentid = ViewParent.Id
view = ViewSection.CreateCallout (doc,ViewParentid,ViewFamilyTypeId,Point1,Point2)
t.Commit()