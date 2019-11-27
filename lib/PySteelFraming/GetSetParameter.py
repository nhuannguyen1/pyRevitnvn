from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,UnitType
import rpw
#from PySteelFraming.SteelFramingCSV import keys,Handling_DataS_Tr_For_Case_Expect
from SteelFramingCSV import StringProcessing
from ConvertUnitRevit import Convert_length
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
def SetParameterInstance (ElementInstance,ParameterName,ParameterValue):
    ElementInstance = ElementInstance.Symbol
    Parameter = ElementInstance.LookupParameter(ParameterName)
    t = Transaction (doc,"Set parameter")
    t.Start()
    Parameter.Set(ParameterValue)
    t.Commit()
def SetParameterFamilySymbol (FamilySymbol,ParameterName,ParameterValue):
    Parameter = FamilySymbol.LookupParameter(ParameterName)
    t = Transaction (doc,"Set parameter")
    t.Start()
    Parameter.Set(ParameterValue)
    t.Commit()
def GetValueName (symbol,Dict_Arr,Index_Row,path_Conf):
    StringProcessing_HD = StringProcessing(path_Conf)
    keys = StringProcessing_HD.keys
    Value_Check_For_For_Case_Expect = StringProcessing_HD.Handling_DataS_Tr_For_Case_Expect()
    for Value_Arr in Value_Check_For_For_Case_Expect:
        if (int(Value_Arr[0]) - 4) == Index_Row:
            print ("Index_Row",Index_Row)
            try: 
                Parameter1 = symbol.LookupParameter(Value_Arr[2]).AsDouble()
                Parameter2 = symbol.LookupParameter(Value_Arr[3]).AsDouble()
                StringToFillOutLambla = lambda Parameter1,Parameter2: Dict_Arr.get(keys[4]) if (Parameter1 == Parameter2) else Dict_Arr.get(keys[3])
                StringToFillOut = StringToFillOutLambla(Parameter1,Parameter2)
            except:
                print ("check symbol family again")
        else:
            try:
                StringToFillOut = Dict_Arr.get(keys[3])
            except:
                print ("check symbol family again in GetValueName function")
    Parameter_Name_Arr = Dict_Arr.get(keys[2])
    ParameterValue = [[Convert_length(symbol.LookupParameter(vt).AsDouble()),vt] for vt in Parameter_Name_Arr]
    for Ele_Para in ParameterValue:
        StringToFillOuted = StringToFillOut.replace(str(Ele_Para[1]),str(Ele_Para[0]))
        StringToFillOut = StringToFillOuted
    return StringToFillOut