# coding: utf8
__doc__ = """Create sections from selected linear objects"""
__title__ = "CSFO"
__author__ = "pyan.vn"

from Autodesk.Revit.DB import Document, 
                              Line, 
                              FilteredElementCollector, 
                              ViewFamilyType, 
                              ViewFamily, 
                              Element,
                              ViewSection, 
                              Transform, 
                              BoundingBoxXYZ, 
                              XYZ, 
                              BuiltInParameter,
                              Transaction, 
                              View
from Autodesk.Revit.UI import UIDocument
from pyrevit import script, forms
import rpw

uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

logger = script.get_logger()

def Rename(Inputparameter1,Inputparameter2,selected_type):
    collectors = FilteredElementCollector(doc).OfClass(ViewFamilyType)
    _config = script.get_config()
    prefix = _config.get_option('prefix', 'Mur')
    X_Right = float(_config.get_option('X_Right', '1'))
    X_Left = float(_config.get_option('X_Left', '1'))
    Y_Up = float(_config.get_option('Y_Up', '1'))
    Y_Bottom = float(_config.get_option('Y_Bottom', '1'))
    t = Transaction(doc, 'This is my new transaction')
    t.Start()
    # Select an element in Revit
    for element_id in uidoc.Selection.GetElementIds():
        ele = doc.GetElement(element_id) 
        picked_bb = ele.get_BoundingBox(doc.ActiveView)  
        # Get max and min points of bounding box.
        picked_bb_max = picked_bb.Max
        picked_bb_min = picked_bb.Min
        Point1 = XYZ(picked_bb_min.X -X_Left,picked_bb_min.Y - Y_Bottom,0)
        Point2 = XYZ(picked_bb_max.X +X_Right,picked_bb_max.Y + Y_Up,0)
        ViewParent = doc.ActiveView
        ViewParentid = ViewParent.Id
        view = ViewSection.CreateCallout (doc,ViewParentid,selected_type.Id,Point1,Point2)
        view.Name = RenameNameView (Inputparameter1,Inputparameter2)
        Inputparameter2 = str(int(Inputparameter2)+ 1)
    t.Commit()
def RenameNameView(Inputparameter1,Inputparameter2):
    InputparameterTotal = Inputparameter1 + Inputparameter2
    ColViews = FilteredElementCollector(doc).OfClass(View)
    a=0
    while True:
        restart = False
        for colview in ColViews:
            if colview.Name == InputparameterTotal:
                a =+ 1
                Inputparameter2 =int(Inputparameter2) + int(a)
                InputparameterTotal = Inputparameter1 + str(Inputparameter2)
                restart = True
                break
        if not restart:
            break
    return InputparameterTotal
class SectionTypeSelection(forms.WPFWindow):
    def __init__(self):
        forms.WPFWindow.__init__(self, "SectionTypeSelection.xaml")

        self.combob_selector.DataContext = \
            [vt for vt in FilteredElementCollector(doc).OfClass(ViewFamilyType) if vt.FamilyName == "Structural Plan"]
        self.selected_type = None
    def Button_Click(self, sender, e):
        self.selected_type = self.combob_selector.SelectedItem
        self.Close()
        self.Input_Parameter1 = self.Input_Parameter1.Text
        self.Input_Parameter2 = self.Input_Parameter2.Text
        Rename(self.Input_Parameter1,self.Input_Parameter2,self.selected_type)
    def show_dialog(self):
        self.ShowDialog()
        if self.selected_type:
            return self.selected_type
        else:
            import sys
            sys.exit()
section_type = SectionTypeSelection().show_dialog()
