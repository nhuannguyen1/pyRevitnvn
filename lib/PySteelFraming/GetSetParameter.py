from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,UnitType
import rpw
from PySteelFraming.SteelFramingCSV import ReturnDataAllRowByIndexpath,CreateDict,keys,Handling_DataS_Tr_For_Case_Expect
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
def GetValueName (symbol,Dict_Arr,Index_Row):
    Value_Check_For_For_Case_Expect = Handling_DataS_Tr_For_Case_Expect()
    print ("Value_Check_For_For_Case_Expect",Value_Check_For_For_Case_Expect)
    for Value_Arr in Value_Check_For_For_Case_Expect:
        if (int(Value_Arr[0]) - 4) == Index_Row:
            print ("Value_Arr",Value_Arr)
            print ("Value_Arr[2],Value_Arr[3]",Value_Arr[2],Value_Arr[3])
            Parameter1 = symbol.LookupParameter(Value_Arr[2]).AsDouble()
            Parameter2 = symbol.LookupParameter(Value_Arr[3]).AsDouble()
            StringToFillOut = lambda x: Dict_Arr.get(keys[4]) if (Parameter1 == Parameter2) else Dict_Arr.get(keys[4])
            print (StringToFillOut)
        else:
            StringToFillOut = Dict_Arr.get(keys[3])
            """
            if Parameter1 == Parameter2:
                StringToFillOut = Dict_Arr.get(keys[int(Value_Arr[4])])
            else:
                StringToFillOut = Dict_Arr.get(keys[int(Value_Arr[3])]
            """
    Parameter_Name_Arr = Dict_Arr.get(keys[2])
    ParameterValue = [[Convert_length(symbol.LookupParameter(vt).AsDouble()),vt] for vt in Parameter_Name_Arr]
    for Ele_Para in ParameterValue:
        StringToFillOuted = StringToFillOut.replace(str(Ele_Para[1]),str(Ele_Para[0]))
        StringToFillOut = StringToFillOuted
    return StringToFillOut