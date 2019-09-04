from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId
import rpw
import csv
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
    #Slope1 = ElementInstance.LookupParameter('Slope').AsDouble()
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

    h_n = H13r_L - Tw1 / 2 + Pl_Total
    G2_V1= V4u + math.cos(Slope) * Tf + math.sin(Slope) * Pl_Total
    V34 = v34u - V4u
    h_t = V34 + G2_V1
    h_n1 = UnitUtils.ConvertFromInternalUnits (h_n, DisplayUnitType.DUT_MILLIMETERS)
    h_t1 = UnitUtils.ConvertFromInternalUnits (h_t, DisplayUnitType.DUT_MILLIMETERS)
    Slope1 = UnitUtils.ConvertFromInternalUnits (Slope, DisplayUnitType.DUT_MILLIMETERS)
    print (h_n1)
    print (h_t1)
    print (Slope1)
    return [h_n,h_t]
def setparameterfromvalue (elemeninstance,ValueName,setvalue):
    Tw2_Rafter = elemeninstance.LookupParameter(ValueName)
    Tw2_Rafter.Set(setvalue)
def writefilecsv(Cout_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n,path,a):
    t = Transaction(doc, 'Write an external file.')
    t.Start()
    row = [str(Cout_Continue), str(Rafter_Family_Lefted.Id), Rafter_Type_Lefted.Id,str(Length_Rater_Lefted_n) ]
    with open(path, 'r') as readFile:
        a = sum (1 for row in readFile)
    if a == 0 or Cout_Continue >= a:
        with open(path, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    t.Commit()
def Getcontentdata (count_Continue,path):
    with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if int(row[0]) == count_Continue:
                    arr = []
                    count_Continue = int(row[0])
                    Rafter_Family_Lefted = doc.GetElement(ElementId(int(row[1])))
                    Rafter_Type_Lefted = doc.GetElement(ElementId(int(row[2])))
                    Length_Rater_Lefted_n = float (row[3])
                    arr = [count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n]
    csvFile.close()
    return arr
def count_csv(path):
    with open(path, 'r') as readFile:
        a = sum (1 for row in readFile)
    readFile.close
    return a