__doc__ = "Framing Steel House"
__author__ = 'NGUYEN VAN NHUAN'
__title__ = 'FramingSTeelHouse'
# -*- coding: UTF-8 -*-
from Autodesk.Revit.DB import Transaction, BuiltInParameter, Element, Level, MEPCurve, ElementId, FamilyInstance\
    , FilteredElementCollector
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from pyrevit.forms import WPFWindow
from event import CustomizableEvent
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import System.Drawing
import System.Windows.Forms
def clicked():
     print("Hello work")
class WPF_PYTHON(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
    def button1_Click(self, sender, event):
        #ext_event.Raise()
        clicked()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').Show()