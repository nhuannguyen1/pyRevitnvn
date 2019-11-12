from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,UnitType
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
display_unit = unit_format_options.DisplayUnits
symbol_type = unit_format_options.UnitSymbol

def SetParameterInstance (ElementInstance,ParameterName,ParameterValue):
    ElementInstance = ElementInstance.Symbol
    #Parameter = ElementInstance.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_MARK )
    Parameter = ElementInstance.LookupParameter(ParameterName)
    #element.get_Parameter( BuiltInParameter.ALL_MODEL_TYPE_MARK ).AsString()
    t = Transaction (doc,"Set parameter")
    t.Start()
    #Set Parameter value 
    Parameter.Set(ParameterValue)
    t.Commit()
def Convert_length(length):
    Int_Length = (UnitUtils.ConvertFromInternalUnits(float(length), display_unit))
    return int(round(Int_Length))
def SetParameterFamilySymbol (FamilySymbol,ParameterName,ParameterValue):
    #Parameter = ElementInstance.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_MARK )
    Parameter = FamilySymbol.LookupParameter(ParameterName)
    #element.get_Parameter( BuiltInParameter.ALL_MODEL_TYPE_MARK ).AsString()
    t = Transaction (doc,"Set parameter")
    t.Start()
    #Set Parameter value 
    Parameter.Set(ParameterValue)
    t.Commit()
def GetValueName (symbol,Parameter_Name_Arr,StringToFillOut):
    ParameterValue = [[Convert_length(symbol.LookupParameter(vt).AsDouble()),vt] for vt in Parameter_Name_Arr]
    for Ele_Para in ParameterValue:
        StringToFillOuted = StringToFillOut.replace(str(Ele_Para[1]),str(Ele_Para[0]))
        StringToFillOut = StringToFillOuted
    return StringToFillOut