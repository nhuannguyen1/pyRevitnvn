from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
import math 
class Global:
    def  __init__(self, ParameterValue):
        self.ParameterValue = ParameterValue
    def globalparameterchange(self,TypeElement):
        #t = Transaction (doc,"Slope Element")
        #t.Start()
        paramId = GlobalParametersManager.FindByName(doc,"Slope")
        param = doc.GetElement(paramId) 
        kkkk = ConvertToInternalUnits1(self.ParameterValue)
        ParameterValue = kkkk.DUT_DECIMAL_DEGREES1()
        param.SetValue(DoubleParameterValue(ParameterValue))
        Slope = TypeElement.LookupParameter('Slope')
        Slope.AssociateWithGlobalParameter(param.Id)
        #t.Commit()
class ConvertToInternalUnits1:
    def  __init__(self, ParameterValue):
        self.ParameterValue = ParameterValue
    def DUT_MILLIMETERS1(self):
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_MILLIMETERS)
        return ParameterValue
    def DUT_DECIMAL_DEGREES1(self):
        #print (self.ParameterValue)
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_DECIMAL_DEGREES)
        return ParameterValue
def GetParameterFromSubElement (ElementInstance,Slope):
    Slope = UnitUtils.ConvertToInternalUnits(Slope, DisplayUnitType.DUT_DECIMAL_DEGREES)
    print (Slope)
    #Slope1 = ElementInstance.LookupParameter('Slope').AsDouble()
    Pl_Right = ElementInstance.LookupParameter('Pl_Rafter').AsDouble()

    ElementType =  doc.GetElement(ElementInstance.GetTypeId())

    Tw2_Rafter = ElementType.LookupParameter('Tw2_WF_R').AsDouble()
    
    Tf = ElementType.LookupParameter('Tf').AsDouble()
    Tw1 = ElementType.LookupParameter('Tw1').AsDouble() 
    Tw2 = ElementType.LookupParameter('Tw2').AsDouble() 
    A = ElementType.LookupParameter('A').AsDouble() 
    print ("A is",A)
    Pl_Total =math.cos(Slope) * Pl_Right * 2
    print ("Pl_Right is :",math.cos(Slope))
    
    print ("Pl_Right is :",UnitUtils.ConvertFromInternalUnits (Pl_Right, DisplayUnitType.DUT_MILLIMETERS))

    print ("Pl_Total is :",UnitUtils.ConvertFromInternalUnits (Pl_Total, DisplayUnitType.DUT_MILLIMETERS))


    v34u = math.cos(Slope) * Tw2_Rafter

    print ("v34u is :",UnitUtils.ConvertFromInternalUnits (v34u, DisplayUnitType.DUT_MILLIMETERS))

    V24u = v34u + A

    print ("V24u is :",UnitUtils.ConvertFromInternalUnits (V24u, DisplayUnitType.DUT_MILLIMETERS))


    H13r = Tw2 - (math.tan(Slope) * V24u)

    print ("H13r is :",UnitUtils.ConvertFromInternalUnits (H13r, DisplayUnitType.DUT_MILLIMETERS))
    
    V4u = math.tan(Slope) * H13r
    print ("V4u is :",UnitUtils.ConvertFromInternalUnits (V4u, DisplayUnitType.DUT_MILLIMETERS))



    H13r_L = H13r - math.tan(Slope) * Tf


    print ("H13r_L is :",UnitUtils.ConvertFromInternalUnits (H13r_L, DisplayUnitType.DUT_MILLIMETERS))

    h_n = H13r_L - Tw1 / 2 + Pl_Total
    G2_V1= V4u + math.cos(Slope) * Tf + math.sin(Slope) * Pl_Total
    V34 = v34u - V4u
    h_t = V34 + G2_V1
    h_n1 = UnitUtils.ConvertFromInternalUnits (h_n, DisplayUnitType.DUT_MILLIMETERS)
    h_t1 = UnitUtils.ConvertFromInternalUnits (h_t, DisplayUnitType.DUT_MILLIMETERS)
    Slope1 = UnitUtils.ConvertFromInternalUnits (Slope, DisplayUnitType.DUT_MILLIMETERS)
    print (h_n1)
    print (h_t1)
    #print (Slope)
    print (Slope1)

    return [h_n,h_t]