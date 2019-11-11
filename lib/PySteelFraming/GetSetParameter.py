from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,FamilyInstance,UnitUtils,DisplayUnitType,BuiltInParameter
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
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
