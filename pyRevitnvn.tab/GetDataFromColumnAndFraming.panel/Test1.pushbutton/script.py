from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,Family,Element 
from Autodesk.Revit.UI.Selection import  ObjectType 
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "Set_Config.csv"
full_path = os.path.join(dir_path,filename)
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import PySteelFraming
from PySteelFraming.GetSetParameter import GetValueName,SetParameterFamilySymbol
from PySteelFraming.SteelFramingCSV import StringProcessing
def CreateElement():
    StringProcessing_HL = StringProcessing(full_path)
    keys_Arr = StringProcessing_HL.keys
    ElementDicts = StringProcessing_HL.CreateDict()
    for index, Element_Arr_Dict in enumerate(ElementDicts):
        collectors = [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.Name ==Element_Arr_Dict.get(keys_Arr[0])]
        for collector in collectors:
            for symbolID in collector.GetFamilySymbolIds():
                symbol = doc.GetElement(symbolID) 
                Name_Value = GetValueName(symbol,Element_Arr_Dict,index,full_path)
                SetParameterFamilySymbol(symbol,Element_Arr_Dict.get(keys_Arr[1]),Name_Value)
CreateElement() 