from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
class Global:
    def  __init__(self, ParameterValue):
        self.ParameterValue = ParameterValue
    def GlobalParameter():
        t = Transaction (doc,"Slope Element")
        t.Start()
        paramId = GlobalParametersManager.FindByName(doc, "Slope")
        param = doc.GetElement(paramId) 
        paramtype = type(param)
        ParameterValue = UnitUtils.ConvertToInternalUnits(20, DisplayUnitType.DUT_DECIMAL_DEGREES)
        ParameterValue = ConvertToInternalUnits (ParameterValue)
        param.SetValue (DoubleParameterValue(ParameterValue))
        t.Commit()
    def ConvertToInternalUnits(UNIT):
        ParameterValue = UnitUtils.ConvertToInternalUnits(UNIT, DisplayUnitType.DUT_MILLIMETERS)
        return ParameterValue