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

uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

# set value config for add-in
_config = script.get_config()
prefix = _config.get_option('prefix', 'Mur')
X_Right = float(_config.get_option('X_Right', '1'))
X_Left = float(_config.get_option('X_Left', '1'))
Y_Up = float(_config.get_option('Y_Up', '1'))
Y_Bottom = float(_config.get_option('Y_Bottom', '1'))

def bottom_left_top_right (element_id):
    """ 
    retrieve bottom left and top right
    """
    # Retrieve Element from id 
    ele = doc.GetElement(element_id) 
    # Retrieves a box that circumscribes all geometry of the subelement.
    picked_bb = ele.get_BoundingBox(doc.ActiveView)

    # Get max and min points of bounding box.
    picked_bb_max = picked_bb.Max
    picked_bb_min = picked_bb.Min

    # Get bottom left point and top right point 
    point_bottom_left = XYZ(picked_bb_min.X -X_Left,picked_bb_min.Y - Y_Bottom,0)
    point_top_right = XYZ(picked_bb_max.X +X_Right,picked_bb_max.Y + Y_Up,0)

    return point_bottom_left,point_top_right


def rename_view_from_form(
                          In_param_1,
                          In_param_2,
                          ):
    """ 
    rename view from from user input
    """
    t = Transaction(doc, 'Create view section')
    # start transaction 
    t.Start()

    # Select an element in Revit
    for element_id in uidoc.Selection.GetElementIds():

        point_bottom_left,point_top_right =  bottom_left_top_right(element_id)

        # get active view to put section
        ViewParent = doc.ActiveView

        # get id of viewparent 
        ViewParentid = ViewParent.Id
        
        # get id of type view 
        View_Family_Type_Id =  ViewParent.GetTypeId()
        
        # create callout 
        view = ViewSection.CreateCallout(doc,
                                        ViewParentid,
                                        View_Family_Type_Id,
                                        point_bottom_left,
                                        point_top_right
                                        )

        # Rename view after create 
        view.Name = rename_name_view (In_param_1,
                                      In_param_2
                                      )

        # Increate number 
        In_param_2 = str(int(In_param_2)+ 1)

    # commit transaction 
    t.Commit()


class cre_callout(object):
    def __init__(self,
                 X_Right,
                 X_Left,
                 Y_Up,
                 Y_Bottom,
                 ):

        self.X_Right = X_Right
        self.X_Left = X_Left
        self.Y_Up = Y_Up
        self.Y_Bottom = Y_Bottom
    
    def __call__(self, f):

        def wrapped_f(*args):

            f(*args)

        return wrapped_f

def rename_name_view(In_param_1,
                     In_param_2
                     ):
    """ 
    rename view section in revit 
    """
    param_name = In_param_1 + In_param_2
    ColViews = FilteredElementCollector(doc).OfClass(View)
    a=0
    while True:
        restart = False
        for colview in ColViews:
            if colview.Name == param_name:
                a =+ 1
                Inputparameter2 =int(Inputparameter2) + int(a)
                param_name = In_param_1 + str(In_param_2)
                restart = True
                break
        if not restart:
            break
    return param_name

class SectionTypeSelection(forms.WPFWindow):

    def __init__(self):
        forms.WPFWindow.__init__(self, "SectionTypeSelection.xaml")

    def Button_Click(self, sender, e):
        self.selected_type = self.combob_selector.SelectedItem
        self.Close()
        self.In_param1 = self.Input_Parameter1.Text
        self.In_param2 = self.Input_Parameter2.Text
        # rename type view 
        rename_view_from_form(self.In_param1,self.In_param2)

    def show_dialog(self):
        self.ShowDialog()
section_type = SectionTypeSelection().show_dialog()
