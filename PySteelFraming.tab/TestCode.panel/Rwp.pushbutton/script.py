__doc__ = "Test run Form with button"
__author__ = 'HO VAN CHUONG'
__title__ = 'Form Option\nRWP'
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
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()