from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId
import rpw
import csv
from pyrevit import script
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
def writefilecsv(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n,path,a):
    t = Transaction(doc, 'Write an external file.')
    t.Start()
    row = [str(Count_Continue), str(Rafter_Family_Lefted.Id), Rafter_Type_Lefted.Id,str(Length_Rater_Lefted_n) ]
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
def Return_Row (Cout_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n):
    return  [str(Cout_Continue), str(Rafter_Family_Lefted.Id), str(Rafter_Type_Lefted.Id),str(Length_Rater_Lefted_n)]
def InputDataChangeToCSV(count_Continue,path,row_input):
    with open(path, 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        lines[count_Continue] = row_input
    with open(path, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    writeFile.close()
    readFile.close()
def GetDataFirstRow(path):
    with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if int(row[0]) == 0:
                    return row
    csvFile.close()
def GetcontentdataStr (count_Continue,path):
    with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if int(row[0]) == count_Continue:
                    return row
    csvFile.close()
class DataFromCSV:
    def  __init__(self, Count, FamilyCol, FamilyColType,Base_Level_Col,Top_Level_Col,FamilyRafter,FamilyRafterType,LevelRafter,Length_Rafter,Thinkess_Plate,path,Gird1,Gird2,Slope):
        self.Count = Count
        self.FamilyCol = FamilyCol
        self.FamilyColType = FamilyColType
        self.Base_Level_Col = Base_Level_Col
        self.Top_Level_Col = Top_Level_Col
        self.FamilyRafter = FamilyRafter
        self.FamilyRafterType = FamilyRafterType
        self.LevelRafter = LevelRafter
        self.Length_Rafter = Length_Rafter
        self.Thinkess_Plate = Thinkess_Plate
        self.path = path
        self.Gird1 = Gird1
        self.Gird2 = Gird2
        self.Slope = Slope
    def writefilecsv(self,a):
        t = Transaction(doc, 'Write an external file.')
        t.Start()
        #row = [str(self.Count), str(self.FamilyRafterType.Id), self.FamilyRafterType.Id,str(self.Length_Rafter) ]
        row = [self.Count, self.FamilyCol.Id, self.FamilyColType.Id,self.Base_Level_Col.Id,self.Top_Level_Col.Id,self.FamilyRafter.Id,self.FamilyRafterType.Id,self.LevelRafter.Id,self.Length_Rafter,self.Thinkess_Plate,self.path,self.Gird1.Id,self.Gird2.Id,self.Slope]
        with open(self.path, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        t.Commit()
    def Getcontentdata (self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if int(row[0]) == self.Count:
                    arr = []
                    self.Count = int(row[0])
                    Column_Left = doc.GetElement(ElementId(int(row[1])))
                    FamilyColType = doc.GetElement(ElementId(int(row[2])))
                    Base_Level_Col = doc.GetElement(ElementId(int(row[3])))
                    Top_Level_Col = doc.GetElement(ElementId(int(row[4])))
                    Rafter_Family_Lefted = doc.GetElement(ElementId(int(row[5])))
                    Rafter_Type_Lefted = doc.GetElement(ElementId(int(row[6])))
                    LevelRafter =  Rafter_Type_Lefted = doc.GetElement(ElementId(int(row[7])))
                    Length_Rater_Lefted_n = float (row[8])
                    Thinkess_Plate = float (row[9])
                    Gird1 = doc.GetElement(ElementId(int(row[11])))
                    Gird2 = doc.GetElement(ElementId(int(row[12])))
                    arr = [self.Count, Column_Left, FamilyColType,Base_Level_Col,Top_Level_Col,Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Thinkess_Plate,self.path,Gird1,Gird2,self.Slope]
        csvFile.close()
        return arr
    def count_csv(self):
        with open(self.path, 'r') as readFile:
            a = sum (1 for row in readFile)
        readFile.close
        return a
    def Return_Row (self):
        return  [str(self.Count), str(self.FamilyCol.Id), str(self.FamilyColType.Id),str(self.Base_Level_Col.Id),str(self.Top_Level_Col.Id),\
                    str(self.FamilyRafter.Id),str(self.FamilyRafterType.Id),str(self.LevelRafter.Id),str(self.Length_Rafter),str(self.Thinkess_Plate),str(self.path),str(self.Gird1.Id),str(self.Gird2.Id),str(self.Slope)]
    def InputDataChangeToCSV(self,row_input):
        with open(self.path, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[self.Count] = row_input
        with open(self.path, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        writeFile.close()
        readFile.close()
    def GetcontentdataStr (self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if int(row[0]) == self.Count:
                    return row
        csvFile.close()
class PlaceElementTotal:
    def  __init__(self,Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled,Slope_Type,Level_Rater_Type_Lefted,Rater_Type_Lefted,Getcondination,LEVEL_ELEV_Base_Level,Length_Rater_Lefted):
        self.Base_Leveled = Base_Leveled
        self.Base_Leveled_Point = Base_Leveled_Point
        self.Top_Leveled = Top_Leveled
        self.Column_Typed = Column_Typed
        self.Slope_Type = Slope_Type
        self.Level_Rater_Type_Lefted = Level_Rater_Type_Lefted
        self.Rater_Type_Lefted = Rater_Type_Lefted
        self.Getcondination = Getcondination
        self.LEVEL_ELEV_Base_Level = LEVEL_ELEV_Base_Level
        self.Length_Rater_Lefted = Length_Rater_Lefted
    def PlaceElement (self):
        t = Transaction (doc,"Place Element")
        t.Start()
        ColumnCreate = doc.Create.NewFamilyInstance(self.Base_Leveled_Point, self.Column_Typed,self.Base_Leveled, Structure.StructuralType.NonStructural)
        LIST = GetParameterFromSubElement(ColumnCreate,self.Slope_Type)
        a= Global(self.Slope_Type)
        a.globalparameterchange(ColumnCreate)
        paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLeve.Set(self.Top_Leveled.Id)
        TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
        TopoffsetPam.Set(0)
        H_t = LIST[1]
        H_n = LIST[0]
        Point_Level =XYZ (self.Getcondination.X + H_n,self.Getcondination.Y, H_t)
        #PlaceElementRafter(Point_Level)
        t.Commit()
        return Point_Level
    def PlaceElementRafter (self,Point_Level):
        Elementinstance = doc.Create.NewFamilyInstance(Point_Level,self.Rater_Type_Lefted, self.Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)
        a= Global(self.Slope_Type)
        a.globalparameterchange(Elementinstance)
        setparameterfromvalue(Elementinstance,'Length',self.Length_Rater_Lefted)