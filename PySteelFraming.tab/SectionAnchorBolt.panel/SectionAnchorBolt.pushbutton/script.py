from Autodesk.Revit.DB import*
from Autodesk.Revit.UI import*
from Autodesk.Revit.Attributes import*
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction, BuiltInParameter, Element, Level, MEPCurve, ElementId, FamilyInstance\
    , FilteredElementCollector
from pyrevit.forms import WPFWindow
import rpw
from rpw import revit
from pypevitmep.event import CustomizableEvent

__doc__ = "Change selected elements level without moving it"
__title__ = "Section Anchor Bolt"
__author__ = "Cyril Waechter"
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
doc = revit.doc
uidoc = revit.uidoc
def delete_elements(locp1,locp2):
    t = Transaction (doc,"Move center to center other element")
    t.Start()
    Loc = locp1.Point
    Locnew = locp2.Point
    locp1.Point = Locnew
    t.Commit()
def INTHU():
    print ("ONLY TEXT")


class RotateElementHandler(IExternalEventHandler):
    """Input : function or method. Execute input in a IExternalEventHandler"""
    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
    # Execute method run in Revit API environment.
    # noinspection PyPep8Naming, PyUnusedLocal
    def Execute(self, application):
        try:
            self.do_this()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print "InvalidOperationException catched"
    # noinspection PyMethodMayBeStatic, PyPep8Naming
    def GetName(self):
        return "Execute an function or method in a IExternalHandler"
# Create handler instances. Same class (2 instance) is used to call 2 different method.
around_itself_handler = RotateElementHandler(delete_elements())
# Create ExternalEvent instance which pass these handlers
around_itself_event = ExternalEvent.Create(around_itself_handler)


class ReferenceLevelSelection(WPFWindow):
    """
    GUI used to select a reference level from a list or an object
    """
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
    # noinspection PyUnusedLocal
    def from_object_click1(self, sender, e):
        self.pick1 = uidoc.Selection.PickObject(ObjectType.Element)
    # noinspection PyUnusedLocal
    def from_object_click2(self, sender, e):
        self.pick2 = uidoc.Selection.PickObject(ObjectType.Element)   
    def from_object_click_Ok(self, sender, e):
        self.Close()
        around_itself_event.Raise()
ReferenceLevelSelection('ReferenceLevelSelection.xaml').Show()
#PipeTypeSelectionForm('PipeTypeSelection.xaml').Show()