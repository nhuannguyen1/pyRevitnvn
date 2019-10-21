from Autodesk.Revit.DB import Element,BuiltInCategory,BuiltInParameter,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,Element
import clr
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import math 
class Global:
    def  __init__(self, ParameterValue,ParameterName,Element):
        self.ParameterValue = ParameterValue
        self.ParameterName = ParameterName
        self.Element = Element
    def globalparameterchange(self):
        print (self.ParameterValue,self.ParameterName,self.Element )
        paramId = GlobalParametersManager.FindByName(doc,self.ParameterName)
        param = doc.GetElement(paramId) 
        kkkk = ConvertToInternalUnits(float(self.ParameterValue))
        ParameterValue = kkkk.DUT_DECIMAL_DEGREES1()
        param.SetValue(DoubleParameterValue(ParameterValue))
        Slope = self.Element.LookupParameter("Slope")
        Slope.AssociateWithGlobalParameter(param.Id)
    def SetParameterInstance (self):
        ParameterName = self.Element.LookupParameter(self.ParameterName)
        ParameterValue = UnitUtils.ConvertToInternalUnits(float(self.ParameterValue), DisplayUnitType.DUT_MILLIMETERS)
        ParameterName.Set(ParameterValue)
class ConvertToInternalUnits:
    def  __init__(self, ParameterValue):
        self.ParameterValue = ParameterValue
    def DUT_MILLIMETERS1(self):
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_MILLIMETERS)
        return ParameterValue
    def DUT_DECIMAL_DEGREES1(self):
        #print (self.ParameterValue)
        ParameterValue = UnitUtils.ConvertToInternalUnits(self.ParameterValue, DisplayUnitType.DUT_DECIMAL_DEGREES)
        return ParameterValue
def ConvertToInternalUnitsmm(Parameter):
    Parameter = UnitUtils.ConvertToInternalUnits(float(Parameter), DisplayUnitType.DUT_MILLIMETERS)
    return Parameter
def ConvertToInternalUnitDegree(Parameter):
    Parameter = UnitUtils.ConvertToInternalUnits(float(Parameter), DisplayUnitType.DUT_DECIMAL_DEGREES)
    return Parameter
def setparameterfromvalue (elemeninstance,ValueName,setvalue):
    Tw2_Rafter = elemeninstance.LookupParameter(ValueName)
    Tw2_Rafter.Set(setvalue)
def GetCondinationH_nAndH_V (ElementInstance,Slope,Plate_Column,X_Left_X,X_Right_X,Offset_Top_Level):
    Offset_Top_Level  = ConvertToInternalUnitsmm (Offset_Top_Level)
    Slope = UnitUtils.ConvertToInternalUnits( float(Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
    Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
    Pl_Right = ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
    ElementType =  doc.GetElement(ElementInstance.GetTypeId())
    Tw2_Rafter = ElementType.LookupParameter('Tw2_WF_R').AsDouble()
    Tf = ElementType.LookupParameter('Tf').AsDouble()
    Tw1 = ElementType.LookupParameter('Tw1').AsDouble() 
    Tw2 = ElementType.LookupParameter('Tw2').AsDouble() 
    A = ElementType.LookupParameter('A').AsDouble() 
    Pl_Total =math.cos(Slope) * Pl_Right * 2
    v34u = math.cos(Slope) * Tw2_Rafter
    V24u = v34u + A
    H13r = Tw2 - (math.tan(Slope) * V24u)
    V4u = math.tan(Slope) * H13r
    H13r_L = H13r - math.tan(Slope) * Tf
    h_n = H13r_L - Tw1 / 2 + (Plate_Column * 2)*math.cos(Slope)
    G2_V1= V4u + math.cos(Slope) * Tf + math.sin(Slope) * Pl_Total
    V34 = v34u - V4u
    h_t = V34 + G2_V1  - math.tan(Slope) * Pl_Total + math.sin(Slope) * (Plate_Column * 2)
    return [h_n - X_Left_X + X_Right_X,h_t  + Offset_Top_Level]
def GetCoordinateContinnue (ElementType, Length_Rafter,Thinkess_Plate1,Slope,H_n,H_t):
    FamilyRafterName = ElementType.FamilyName 
    if "4111" in FamilyRafterName:
        H_n = H_n + Length_Rafter * math.cos(Slope)  + Thinkess_Plate1 * 2 
        H_t = H_t + Length_Rafter* math.sin(Slope) + Thinkess_Plate1 * 2 * math.tan(Slope)
    else:
        H_n = H_n + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.cos(Slope) 
        H_t = H_t + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.sin(Slope)
    return [H_n,H_t]
def ConvertFromInteralUnitToMM (Parameter):
    Parameter = UnitUtils.ConvertFromInternalUnits(float(Parameter), DisplayUnitType.DUT_MILLIMETERS)
    return Parameter
def FindV34 (ElementInstance,Slope,Offset_Top_Level,X_Left_X,X_Right_X):
    Offset_Top_Level  = ConvertToInternalUnitsmm (Offset_Top_Level)
    Slope = UnitUtils.ConvertToInternalUnits( float(Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
    #Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
    Pl_Right = ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
    ElementType =  doc.GetElement(ElementInstance.GetTypeId())
    Tw2_Rafter = ElementType.LookupParameter('Tw2_WF_R').AsDouble()
    Tf = ElementType.LookupParameter('Tf').AsDouble()
    Tw1 = ElementType.LookupParameter('Tw1').AsDouble() 
    Tw2 = ElementType.LookupParameter('Tw2').AsDouble() 
    A = ElementType.LookupParameter('A').AsDouble() 
    Pl_Total =math.cos(Slope) * Pl_Right * 2
    v34u = math.cos(Slope) * Tw2_Rafter
    V24u = v34u + A
    H13r = Tw2 - (math.tan(Slope) * V24u)
    V4u = math.tan(Slope) * H13r
    H13r_L = H13r - math.tan(Slope) * Tf
    #h_n = H13r_L - Tw1 / 2 + (Plate_Column * 2)*math.cos(Slope)
    G2_V1= V4u + math.cos(Slope) * Tf + math.sin(Slope) * Pl_Total
    V34 = v34u - V4u 
    MoveDistance = X_Left_X + X_Right_X 
    V_ct = V34 + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope)
    return V_ct
def GetSlope(EH,PH,Length):
    CvLength = ConvertToInternalUnits(Length)
    Length = UnitUtils.ConvertToInternalUnits(float(Length), DisplayUnitType.DUT_MILLIMETERS)
    ElevationEH = EH.Elevation
    ElevationPH = PH.Elevation
    HeighE = float (ElevationPH)  - float(ElevationEH)
    Slope = math.atan(HeighE / Length)
    Slope = UnitUtils.ConvertFromInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
    return Slope
def FindV34_1 (ElementInstance,Slope,Offset_Top_Level,X_Left_X,X_Right_X,CH,PH,Length):
    Offset_Top_Level  = ConvertToInternalUnitsmm (Offset_Top_Level)
    Slope = UnitUtils.ConvertToInternalUnits( float(Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
    #Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
    Pl_Right = ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
    ElementType =  doc.GetElement(ElementInstance.GetTypeId())
    Tw2_Rafter = ElementType.LookupParameter('Tw2_WF_R').AsDouble()
    Tf = ElementType.LookupParameter('Tf').AsDouble()
    Tw1 = ElementType.LookupParameter('Tw1').AsDouble() 
    Tw2 = ElementType.LookupParameter('Tw2').AsDouble() 
    A = ElementType.LookupParameter('A').AsDouble() 
    Pl_Total =math.cos(Slope) * Pl_Right * 2
    v34u = math.cos(Slope) * Tw2_Rafter
    V24u = v34u + A
    H13r = Tw2 - (math.tan(Slope) * V24u)
    V4u = math.tan(Slope) * H13r
    H13r_L = H13r - math.tan(Slope) * Tf
    #h_n = H13r_L - Tw1 / 2 + (Plate_Column * 2)*math.cos(Slope)
    G2_V1= V4u + math.cos(Slope) * Tf + math.sin(Slope) * Pl_Total
    V34 = v34u - V4u 
    MoveDistance = X_Left_X + X_Right_X 
    V_ct = math.cos(Slope) * Tw2_Rafter -  math.tan(Slope) * (Tw2 - (math.tan(Slope) * ( (math.cos(Slope) * Tw2_Rafter) + A))) + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope)
    V_ct = -math.tan(Slope)*L-CH+PH

    k = math.sqrt(1- ((math.cos(Slope))^2/(math.cos(Slope))^2))  # equivation tan

    math.sqrt(1/(k+1))

    - k*L-CH + PH = sqrt(1/(k+1)* Tw2_Rafter -  k * (Tw2 - (k* ( (sqrt(1/(k+1) * Tw2_Rafter) + A))) + Tw1 / 2 * k + Tf/sqrt(1/(k+1) + MoveDistance * k

    sqrt(1/(k+1)* Tw2_Rafter -  k * (Tw2 - (k* ( (sqrt(1/(k+1) * Tw2_Rafter) + A))) + Tw1 / 2 * k + Tf/sqrt(1/(k+1) + MoveDistance * k - ( - k*L-CH + PH )



    return V_ct