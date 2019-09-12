from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId
import rpw
import csv
import clr
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
def GetParameterFromSubElement (ElementInstance,Rafter_Type_Lefted,Slope,Length_Rafter,path,Gird1,Gird2):
    Arr_Point_Type_Length = []
    ArrTotal = []
    #Slope = UnitUtils.ConvertToInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
    Getcondination =  Getintersection (Gird1.Curve,Gird2.Curve)
    LIST =  GetHt_Hn (ElementInstance,Slope)
    Slope = UnitUtils.ConvertToInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
    H_t = LIST[1]
    H_n = LIST[0]

    H_t0 = LIST[1]
    H_n0 = LIST[0]
    
    with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                DataFromCSV_DATA = DataFromCSV(int(row[0]),None,None,None,None,None,Rafter_Type_Lefted,None,Length_Rafter,None,path,None,None,None,None,None,None)
                
                arr = DataFromCSV_DATA.Getcontentdata()
                Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t)
                Arr_Point_Type_Length=[Point_Level,arr[6],arr[8]]
                
                Length_Rafter = arr[8]
                print ("length rapter is",Length_Rafter)
                Length_Rafter = UnitUtils.Convert(Length_Rafter,DisplayUnitType.DUT_MILLIMETERS, DisplayUnitType.DUT_DECIMAL_FEET)

                #print ("length rapter is 1",Length_Rafter1)

                if row[0]==0:
                    H_n = H_n + Length_Rafter * math.cos(Slope)
                    H_t = H_t + Length_Rafter * math.sin(Slope)
                    ArrTotal.append(Arr_Point_Type_Length)
                else:
                    H_n = H_n + Length_Rafter * math.cos(Slope)
                    H_t = H_t + Length_Rafter * math.sin(Slope)
                    ArrTotal.append(Arr_Point_Type_Length)
            return ArrTotal
    csvFile.close()
def GetHt_Hn (ElementInstance,Slope):

    Slope = UnitUtils.ConvertToInternalUnits(Slope, DisplayUnitType.DUT_DECIMAL_DEGREES)

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
    return [h_n,h_t]
def setparameterfromvalue (elemeninstance,ValueName,setvalue):
    Tw2_Rafter = elemeninstance.LookupParameter(ValueName)
    Tw2_Rafter.Set(setvalue)
class DataFromCSV:
    def  __init__(self, Count, FamilyCol, FamilyColType,Base_Level_Col,Top_Level_Col,FamilyRafter,FamilyRafterType,LevelRafter,Length_Rafter,\
        Thinkess_Plate,path,Gird1,Gird2,Slope,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Gird):
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
        self.Gird_Ver_Ged = Gird_Ver_Ged
        self.Gird_Hor_Ged = Gird_Hor_Ged
        self.Length_From_Gird = Length_From_Gird

    def writefilecsv(self,a):
        t = Transaction(doc, 'Write an external file.')
        t.Start()
        #row = [str(self.Count), str(self.FamilyRafterType.Id), self.FamilyRafterType.Id,str(self.Length_Rafter) ]
        row = [self.Count, self.FamilyCol.Id, self.FamilyColType.Id,self.Base_Level_Col.Id,self.Top_Level_Col.Id,\
            self.FamilyRafter.Id,self.FamilyRafterType.Id,self.LevelRafter.Id,self.Length_Rafter,\
                self.Thinkess_Plate,self.path,self.Gird1.Id,self.Gird2.Id,self.Slope,self.Gird_Ver_Ged.Id,self.Gird_Hor_Ged.Id,self.Length_From_Gird]
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
                    LevelRafter = doc.GetElement(ElementId(int(row[7])))
                    Length_Rater_Lefted_n = float (row[8])
                    Thinkess_Plate = float (row[9])
                    Gird1 = doc.GetElement(ElementId(int(row[11])))
                    Gird2 = doc.GetElement(ElementId(int(row[12])))
                    Slope = float (row[13])
                    Gird_Ver_G = doc.GetElement(ElementId(int(row[14])))
                    Gird_Hor_G = doc.GetElement(ElementId(int(row[15])))
                    Length_From_Gird = float (row[16])
                    arr = [self.Count, Column_Left, FamilyColType,Base_Level_Col,Top_Level_Col,Rafter_Family_Lefted,\
                        Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Thinkess_Plate,self.path,Gird1,Gird2,Slope,\
                            Gird_Ver_G,Gird_Hor_G,Length_From_Gird]
        csvFile.close()
        return arr
    def count_csv(self):
        with open(self.path, 'r') as readFile:
            a = sum (1 for row in readFile)
        readFile.close
        return a
    def Return_Row (self):
        return  [str(self.Count), str(self.FamilyCol.Id), str(self.FamilyColType.Id),str(self.Base_Level_Col.Id),str(self.Top_Level_Col.Id),\
                    str(self.FamilyRafter.Id),str(self.FamilyRafterType.Id),str(self.LevelRafter.Id),str(self.Length_Rafter),\
                        str(self.Thinkess_Plate),str(self.path),str(self.Gird1.Id),str(self.Gird2.Id),str(self.Slope),str(self.Gird_Ver_Ged.Id),\
                            str(self.Gird_Hor_Ged.Id),str(self.Length_From_Gird)]
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
    def PlaceElement (self):
        self.Length_Rafter = (UnitUtils.ConvertToInternalUnits(float(self.Length_Rafter), DisplayUnitType.DUT_MILLIMETERS))
        LEVEL_ELEV_Base_Level= self.Top_Level_Col.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        Getcondination =  Getintersection (self.Gird1.Curve,self.Gird2.Curve)
        Base_Leveled_Point =XYZ (Getcondination.X,Getcondination.Y,(LEVEL_ELEV_Base_Level))
        #t = Transaction (doc,"Place Element")
        #t.Start()
        ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, self.FamilyColType,self.Base_Level_Col, Structure.StructuralType.NonStructural)
        #LIST = GetParameterFromSubElement(ColumnCreate,self.Slope)
        a= Global(self.Slope)
        a.globalparameterchange(ColumnCreate)
        paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLeve.Set(self.Top_Level_Col.Id)
        TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
        TopoffsetPam.Set(0)
        #t.Commit()
        return ColumnCreate
    def PlaceElementRafterFather(self,ColumnCreate):
        #GetParameterFromSubElement (ElementInstance,Rafter_Type_Lefted,Slope,Length_Rafter,path,Gird1,Gird2):
        Point_Levels = GetParameterFromSubElement (ColumnCreate,self.FamilyRafterType,self.Slope,self.Length_Rafter,self.path,self.Gird1,self.Gird2)
        for Point_Level,FamilyRafterType,Length_Rafter in Point_Levels:
            Length_Rafter = UnitUtils.ConvertToInternalUnits(float(Length_Rafter), DisplayUnitType.DUT_MILLIMETERS)
            PlaceElementRafter(Point_Level,FamilyRafterType,self.LevelRafter,Length_Rafter,self.Slope)
    def DeleteRow(self):
        with open(self.path ,'rb') as inp:
            for row in csv.reader(inp):
                if int(row[0]) == self.Count:
                    ClearRow = [row]
        with open(self.path, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(ClearRow)
    def checkLengthOfItemRafter (self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            sum = 0 
            for row in readcsv:
                sum = sum + float(row[16]) 
        csvFile.close()
        if (self.Length_From_Gird) < sum:
            print ("Recheck Total Length of Rafter")
def PlaceElementRafter (Point_Level,Rater_Type_Lefted,Level_Rater_Type_Lefted,Length_Rater_Lefted,Slope_Type):
    Elementinstance = doc.Create.NewFamilyInstance(Point_Level,Rater_Type_Lefted, Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)
    a= Global(Slope_Type)
    a.globalparameterchange(Elementinstance)
    setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
def Getintersection (line1, line2):
    results = clr.Reference[IntersectionResultArray]()
    result = line1.Intersect(line2, results)
    if result != SetComparisonResult.Overlap:
	    print('No Intesection, Review Gird was chose')
    res = results.Item[0]
    return res.XYZPoint
