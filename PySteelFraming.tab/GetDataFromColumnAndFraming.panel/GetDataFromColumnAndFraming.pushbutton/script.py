from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,Family,Element 
from Autodesk.Revit.UI.Selection import  ObjectType 
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import PySteelFraming
from PySteelFraming.GetSetParameter import SetParameterInstance
from PySteelFraming.SteelFramingCSV import ReturnDataAllRowByIndexpath
from PySteelFraming.SteelFramingCSV import CreateDict

#a = ReturnDataAllRowByIndexpath(1)
def CreateElement():
    """
    collectors = FilteredElementCollector(doc)
    collectors.OfClass(Family).ToElements()
    """
    for Element_Arr_Dict in CreateDict:

        collectors = [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.Name == "4111a.Rafter-Tapper-Vertical-Left_Tool"]
        for collector in collectors:
            for symbolID in collector.GetFamilySymbolIds():
                symbol = doc.GetElement(symbolID) 
                print (Element.Name.__get__(symbol))
        
    """
    for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilyInstance):
        
        SetParameterInstance(vt,"Description","Description_Description")
    """
CreateElement()