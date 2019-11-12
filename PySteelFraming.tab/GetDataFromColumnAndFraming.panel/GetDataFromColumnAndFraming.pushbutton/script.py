from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,Family,Element 
from Autodesk.Revit.UI.Selection import  ObjectType 
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import PySteelFraming
from PySteelFraming.GetSetParameter import SetParameterInstance,SetParameterFamilySymbol,GetValueName
from PySteelFraming.SteelFramingCSV import ReturnDataAllRowByIndexpath,CreateDict,keys
from PySteelFraming.DirectoryPath import dir_path
def CreateElement():
    ElementDicts = CreateDict()
    for Element_Arr_Dict in ElementDicts:
        collectors = [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.Name ==Element_Arr_Dict.get(keys[0])]
        for collector in collectors:
            for symbolID in collector.GetFamilySymbolIds():
                symbol = doc.GetElement(symbolID) 
                Name_Value = GetValueName(symbol,Element_Arr_Dict.get(keys[2]),Element_Arr_Dict.get(keys[3]))
                SetParameterFamilySymbol(symbol,Element_Arr_Dict.get(keys[1]),Name_Value)
CreateElement()