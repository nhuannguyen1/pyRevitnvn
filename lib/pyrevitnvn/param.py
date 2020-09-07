from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter,UnitType
#from PySteelFraming.SteelFramingCSV import keys,Handling_DataS_Tr_For_Case_Expect
from SteelFramingCSV import StringProcessing
from ConvertUnitRevit import Convert_length
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
def SetParameterInstance (ElementInstance,
                         ParameterName,
                         ParameterValue
                         ):
    ElementInstance = ElementInstance.Symbol
    Parameter = ElementInstance.LookupParameter(ParameterName)
    t = Transaction (doc,"Set parameter")
    t.Start()
    Parameter.Set(ParameterValue)
    t.Commit()

def set_param_from_symbol (FamilySymbol,
                           ParameterName,
                           ParameterValue
                           ):
    """ set param from symbol """

    Parameter = FamilySymbol.LookupParameter(ParameterName)
    t = Transaction (doc,"Set parameter")
    t.Start()
    Parameter.Set(ParameterValue)
    t.Commit()

def get_value_name (symbol,
                    Dict_Arr,
                    Index_Row,
                    ):

    # get key value 
    keys = sorted(Dict_Arr.keys())
    Parameter_Name_Arr = Dict_Arr.get(keys[2])
    ParameterValue = [[Convert_length(symbol.LookupParameter(vt).AsDouble()),vt] for vt in Parameter_Name_Arr]
    
    StringToFillOut = Dict_Arr.get(keys[3])

    for Ele_Para in ParameterValue:
        
        StringToFillOuted = StringToFillOut.replace(str(Ele_Para[1]),
                                                    str(Ele_Para[0])
                                                    )
                
        StringToFillOut = StringToFillOuted
    return StringToFillOut