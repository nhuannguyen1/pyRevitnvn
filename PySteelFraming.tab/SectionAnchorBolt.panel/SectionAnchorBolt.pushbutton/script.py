# coding: utf8

__doc__ = """Create sections from selected linear objects (eg. walls)
SHIFT-CLICK to display options"""
__title__ = "CreateSectionFrom"
__author__ = "Cyril Waechter"

from Autodesk.Revit.DB import Document, Line, FilteredElementCollector, ViewFamilyType, ViewFamily, Element, \
    ViewSection, Transform, BoundingBoxXYZ, XYZ, BuiltInParameter,Transaction
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit import Exceptions

from pyrevit import script, forms
import rpw

uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
t = Transaction (doc,"Place Element")
t.Start()
collectors = FilteredElementCollector(doc).OfClass(ViewFamilyType)
for collector in collectors:
    tn = Element.Name.__get__(collector)
    if tn == 'IIa.Detail Anchor Bolt':
        ViewFamilyTypeId = collector.Id     
Point1 = XYZ(2,2,2)
Point2 = XYZ(15,15,15)
ViewParent = doc.ActiveView
ViewParentid = ViewParent.Id
view = ViewSection.CreateCallout (doc,ViewParentid,ViewFamilyTypeId,Point1,Point2)
t.Commit()