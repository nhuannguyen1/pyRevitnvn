from Autodesk.Revit.DB import Element,BuiltInCategory,BuiltInParameter,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,Element
import clr
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import math 
#from DirectoryPath import Path_Config_Setting
from Csv_Steel.Csv_Connect_Data import DataCSV
class Global:
    def  __init__(self, ParameterValue,ParameterName,Element):
        self.ParameterValue = ParameterValue
        self.ParameterName = ParameterName
        self.Element = Element
    def globalparameterchange(self):
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
def GetParamaterFromElementType(FamilySymbol,ParameterName):
    ParameterValue = FamilySymbol.LookupParameter(ParameterName).AsDouble()
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

class CaculateForFraming:
    def  __init__(self, ElementInstance = None,ElementType= None,Slope = None,Plate_Column = None,\
        X_Left_X= None,X_Right_X= None,Offset_Top_Level = None,Thinkess_Plate1 = None,\
            H_n = None,H_t = None,LengthPurlin = None,CH = None, EH = None, PH = None,Length = None,Length_Rafter= None, ElevationEH = None, ElevationPH = None, path = None, Path_Config_Setting = None):
        self.ElementInstance = ElementInstance 
        self.ElementType = ElementType
        self.Slope = Slope
        self.Plate_Column = Plate_Column
        self.X_Left_X = X_Left_X
        self.X_Right_X = X_Right_X
        self.Offset_Top_Level = Offset_Top_Level
        self.Thinkess_Plate1 = Thinkess_Plate1
        self.H_n = H_n
        self.H_t = H_t
        self.LengthPurlin = LengthPurlin
        self.CH = CH
        self.EH = EH
        self.PH = PH
        self.Length = Length
        self.Length_Rafter = Length_Rafter
        self.ElevationEH = ElevationEH
        self.ElevationPH = ElevationPH
        self.path = path
        self.Path_Config_Setting  = Path_Config_Setting 
    def GetCondinationH_nAndH_V (self):
        Offset_Top_Level  = ConvertToInternalUnitsmm (self.Offset_Top_Level)
        Slope = UnitUtils.ConvertToInternalUnits( float(self.Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
        Plate_Column  = ConvertToInternalUnitsmm (self.Plate_Column)
        Pl_Right = self.ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
        ElementType =  doc.GetElement(self.ElementInstance.GetTypeId())
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
        return [h_n - self.X_Left_X + self.X_Right_X, h_t  + Offset_Top_Level]
    def GetCoordinateContinnue (self):
        FamilyRafterName = self.ElementType.FamilyName 
        if "4111" in FamilyRafterName:
            H_n = self.H_n + self.Length_Rafter  * math.cos(self.Slope)  + self.Thinkess_Plate1 * 2 
            H_t = self.H_t + self.Length_Rafter * math.sin(self.Slope) + self.Thinkess_Plate1 * 2 * math.tan(self.Slope)
        else:
            H_n = self.H_n + (self.Length_Rafter  + self.Thinkess_Plate1 * 2 ) * math.cos(self.Slope) 
            H_t = self.H_t + (self.Length_Rafter  + self.Thinkess_Plate1 * 2 ) * math.sin(self.Slope)
        return [H_n,H_t]

    def FindV34 (self):
        Slope = UnitUtils.ConvertToInternalUnits( float(self.Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
        #Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
        Pl_Right = self.ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
        ElementType =  doc.GetElement(self.ElementInstance.GetTypeId())
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
        MoveDistance = self.X_Left_X + self.X_Right_X 

        print ("self.LengthPurlin ",self.LengthPurlin )

        V_ct = V34 + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope) + self.LengthPurlin / math.cos(Slope)
        return V_ct
    def GetSlope(self):
        Length = UnitUtils.ConvertToInternalUnits(float(self.Length), DisplayUnitType.DUT_MILLIMETERS)
        ElevationEH = self.EH.Elevation
        ElevationPH = self.PH.Elevation
        HeighE = float (ElevationPH)  - float(ElevationEH)
        Slope = math.atan(HeighE / Length)
        Slope = UnitUtils.ConvertFromInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        return Slope
    def FindSlopeFromPHandEV (self):
        #Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
        ElementType =  doc.GetElement(self.ElementInstance.GetTypeId())
        Tw2_Rafter = ElementType.LookupParameter('Tw2_WF_R').AsDouble()
        Tf = ElementType.LookupParameter('Tf').AsDouble()
        Tw1 = ElementType.LookupParameter('Tw1').AsDouble() 
        Tw2 = ElementType.LookupParameter('Tw2').AsDouble() 
        A = ElementType.LookupParameter('A').AsDouble() 
        Length = UnitUtils.ConvertToInternalUnits(float(self.Length), DisplayUnitType.DUT_MILLIMETERS)
        MoveDistance = self.X_Left_X + self.X_Right_X 
        CheckConfig = DataCSV(self.Path_Config_Setting)
        ArrCheckConfig = CheckConfig.ReturnDataAllRowByIndexpath(self.Path_Config_Setting ,6)
        if ArrCheckConfig[1] == "Top_Rafter":
            for i in frange (3,30,0.01):
                Slope = UnitUtils.ConvertToInternalUnits( float(i) , DisplayUnitType.DUT_DECIMAL_DEGREES)
                V1 = - math.tan(Slope)* Length - self.CH + self.PH
                V2 = math.cos(Slope) * Tw2_Rafter - math.tan(Slope) * ( Tw2 - (math.tan(Slope) * (( math.cos(Slope) * Tw2_Rafter) + A))) + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope)
                if round(V1,1) == round(V2,1):
                    break  
        else:
            for i in frange (3,30,0.01):
                Slope = UnitUtils.ConvertToInternalUnits( float(i) , DisplayUnitType.DUT_DECIMAL_DEGREES)
                V1 = - math.tan(Slope)* Length - float(self.CH) + float(self.PH) - (float(self.LengthPurlin) / math.cos(Slope))
                V2 = math.cos(Slope) * Tw2_Rafter - math.tan(Slope) * ( Tw2 - (math.tan(Slope) * (( math.cos(Slope) * Tw2_Rafter) + A))) + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope)
                if round(V1,1) == round(V2,1):
                    break
        return [i,V1]
    def GetSlopetEhAndPh(self):
        Length = UnitUtils.ConvertToInternalUnits(float(self.Length), DisplayUnitType.DUT_MILLIMETERS)
        HeighE = float (self.PH)  - float(self.EH)
        Slope = math.atan(HeighE / Length)
        Slope = UnitUtils.ConvertFromInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        PH1 = UnitUtils.ConvertFromInternalUnits(float(self.PH), DisplayUnitType.DUT_MILLIMETERS)
        return Slope
    def FindX_RightAndX_Left (self):
        Slope = UnitUtils.ConvertToInternalUnits( float(self.Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
        Length = UnitUtils.ConvertToInternalUnits(float(self.Length), DisplayUnitType.DUT_MILLIMETERS)
        HeighE = self.ElevationPH - self.ElevationEH 
        lengthFl = HeighE / math.tan(Slope)
        X_MD = lengthFl - Length
        lengthFlt1 = UnitUtils.ConvertFromInternalUnits(float(Length), DisplayUnitType.DUT_MILLIMETERS)
        x_MD = UnitUtils.ConvertFromInternalUnits(float(X_MD), DisplayUnitType.DUT_MILLIMETERS)
        if X_MD > 0:
            X_Right_X = 0
            X_Left_X = X_MD 
        else:
            X_Right_X = - float(X_MD) 
            X_Left_X = 0
        return [X_Left_X,X_Right_X]
    def FindOffsetLevel (self):
        Length = UnitUtils.ConvertToInternalUnits(float(self.Length), DisplayUnitType.DUT_MILLIMETERS)
        Offset_Top_Level  = ConvertToInternalUnitsmm (self.Offset_Top_Level)
        Slope = UnitUtils.ConvertToInternalUnits( float(self.Slope) , DisplayUnitType.DUT_DECIMAL_DEGREES)
        #Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
        Pl_Right = self.ElementInstance.LookupParameter('Pl_Rafter').AsDouble()
        ElementType =  doc.GetElement(self.ElementInstance.GetTypeId())
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
        MoveDistance = self.X_Left_X + self.X_Right_X 
        if self.X_Left_X > self.X_Right_X:
            V_ct = V34 + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope)) + MoveDistance * math.tan(Slope)
            Length_Dis = (self.ElevationEH + V_ct + math.tan(Slope) * Length) - self.ElevationPH
        else:
            V_ct = V34 + Tw1 / 2 * math.tan(Slope) + Tf/(math.cos(Slope))
            Length_Dis = - (self.ElevationPH -  (self.ElevationEH + V_ct + math.tan(Slope) * (Length - MoveDistance)))
        return  Length_Dis
def ConvertFromInteralUnitToMM (Parameter):
    Parameter = UnitUtils.ConvertFromInternalUnits(float(Parameter), DisplayUnitType.DUT_MILLIMETERS)
    return Parameter
def frange(start, stop=None, step=None):
    #Use float number in range() function
    # if stop and step argument is null set start=0.0 and step = 1.0
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield ("%g" % start) # return float number
        start = start + step