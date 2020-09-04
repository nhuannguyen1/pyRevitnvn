# coding: utf8
__doc__ = """Create sections from selected linear objects SHIFT-CLICK to display option"""
__title__ = "CSFO"
__author__ = "pyan.vn"

from Autodesk.Revit.DB import (Document, 
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
                              View)
from Autodesk.Revit.UI import UIDocument
from pyrevit import script, forms
import rpw
import sys
from pyrevitnvn.view import cre_callout
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

# set value config for add-in
_config = script.get_config()
prefix = _config.get_option('prefix', 'Mur')
X_Right = float(_config.get_option('X_Right', '1'))
X_Left = float(_config.get_option('X_Left', '1'))
Y_Up = float(_config.get_option('Y_Up', '1'))
Y_Bottom = float(_config.get_option('Y_Bottom', '1'))

@cre_callout(X_Right,X_Left,Y_Up,Y_Bottom)
def rename_name_view(In_param_1,
                     In_param_2
                     ):
    
    """ 
    rename view callout in revit 
    """
    # get view name by user 
    param_name = In_param_1 + In_param_2

    while True:
        restart = False
        for colview in FilteredElementCollector(doc).OfClass(View):
            if colview.Name == param_name:
                a = +1 
                In_param_2 = int(In_param_2) + a
                param_name = In_param_1 + str( In_param_2)
                restart = True
                break
        if not restart:
            break
    return param_name
class SectionTypeSelection(forms.WPFWindow):
    """ 
    Create forms for  add-in from WPF
    """
    def __init__(self):
        forms.WPFWindow.__init__(self, "SectionTypeSelection.xaml")

    def Button_Click(self, sender, e):
        # Close from if click button
        self.Close()
        # get input praameter 1
        self.In_param1 = self.Input_Parameter1.Text
        # get input praameter 2
        self.In_param2 = self.Input_Parameter2.Text
        # rename type view 
        rename_name_view(self.In_param1,self.In_param2)

    def show_dialog(self):
        self.ShowDialog()

section_type = SectionTypeSelection().show_dialog()
