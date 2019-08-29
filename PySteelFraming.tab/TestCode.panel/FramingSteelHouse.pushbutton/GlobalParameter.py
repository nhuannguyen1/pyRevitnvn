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
    def globalparameterchange(ParameterValue):
        t = Transaction (doc,"Slope Element")
        t.Start()
        paramId = GlobalParametersManager.FindByName(doc,"Slope")
        param = doc.GetElement(paramId) 
        kkkk = ConvertToInternalUnits(ParameterValue)
        ParameterValue = kkkk.DUT_DECIMAL_DEGREES()
        print (ParameterValue)
        param.SetValue(DoubleParameterValue(ParameterValue))
        t.Commit()
class ConvertToInternalUnits:
    def  __init__(self, ParameterValue):
        self.ParameterValue = ParameterValue
    def DUT_MILLIMETERS(self):
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_MILLIMETERS)
        return ParameterValue
    def DUT_DECIMAL_DEGREES(self):
        print (self.ParameterValue)
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_DECIMAL_DEGREES)
        return ParameterValue
    


"""
def ConvertToInternalUnits(UNIT):
    ParameterValue = UnitUtils.ConvertToInternalUnits(UNIT, DisplayUnitType.DUT_MILLIMETERS)
    return ParameterValue
def GlobalParameter():
    t = Transaction (doc,"Slope Element")
    t.Start()
    paramId = GlobalParametersManager.FindByName(doc, "Slope")
    param = doc.GetElement(paramId) 
    paramtype = type(param)
    ParameterValue = UnitUtils.ConvertToInternalUnits(20, DisplayUnitType.DUT_DECIMAL_DEGREES)
    param.SetValue (DoubleParameterValue(ParameterValue))
    t.Commit()
"""