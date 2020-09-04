from Autodesk.Revit.DB import (Document, 
                              Element,
                              ViewSection, 
                              XYZ, 
                              Transaction, 
                              View)
from Autodesk.Revit.UI import UIDocument
from pyrevit import script
import rpw

uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

def bottom_left_top_right (element_id,
                           X_Right,
                           X_Left,
                           Y_Up,
                           Y_Bottom
                           ):

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
            t = Transaction(doc, 'Create view section')
            
            # Select an element in Revit
            for element_id in uidoc.Selection.GetElementIds():

                point_bottom_left,point_top_right =  bottom_left_top_right(element_id,
                                                                           X_Right=self.X_Right,
                                                                           X_Left=self.X_Left,
                                                                           Y_Up=self.Y_Up,
                                                                           Y_Bottom=self.Y_Bottom
                                                                           )

                # get active view to put section
                ViewParent = doc.ActiveView

                # get id of viewparent 
                ViewParentid = ViewParent.Id
        
                # get id of type view 
                View_Family_Type_Id =  ViewParent.GetTypeId()
                
                # start transaction 
                t.Start()

                # create callout 
                view = ViewSection.CreateCallout(doc,
                                                ViewParentid,
                                                View_Family_Type_Id,
                                                point_bottom_left,
                                                point_top_right
                                                )

                # Rename view after create 
                In_param_1,In_param_2 = args
                view.Name = f(In_param_1,In_param_2)

                # Increate number 
                In_param_2 = str(int(In_param_2)+ 1)

                # commit transaction 
                t.Commit()

        return wrapped_f
