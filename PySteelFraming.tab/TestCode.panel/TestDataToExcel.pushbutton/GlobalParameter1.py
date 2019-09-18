from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId
import rpw
import csv
import clr
from pyrevit import script
# import the Excel Interop. 
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
import math 
import xlrd 

clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal
ex = Excel.ApplicationClass()   
ex.Visible = True
ex.DisplayAlerts = False 

GetContentDataFromExcelArr = []
_config = script.get_config()
X_Top_X = float(_config.get_option('X_Top_X', '1'))
X_Bottom_X = float(_config.get_option('X_Bottom_X', '1'))
X_Left_X = float(_config.get_option('X_Left_X', '1'))
X_Right_X = float(_config.get_option('X_Right_X', '1'))


path_excel1 = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\ExcelTest8.xlsx"



class Global:
    def  __init__(self, ParameterValue,ParameterName,Element):
        self.ParameterValue = ParameterValue
        self.ParameterName = ParameterName
        self.Element = Element
        
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
    def SetParameterInstance (self):
        ParameterName = self.Element.LookupParameter(self.ParameterName)
        ParameterValue = UnitUtils.ConvertToInternalUnits(float(self.ParameterValue), DisplayUnitType.DUT_MILLIMETERS)
        ParameterName.Set(ParameterValue)
        #t.Commit()
def ConvertToInternalUnitsmm(Parameter):
    Parameter = UnitUtils.ConvertToInternalUnits(float(Parameter), DisplayUnitType.DUT_MILLIMETERS)
    return Parameter
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
def GetParameterFromSubElement (ElementInstance,Rafter_Type_Lefted,Slope,Length_Rafter,path,Gird1,Gird2,Thinkess_Plate,Plate_Column):
    
    Arr_Point_Type_Length = []
    ArrTotal = []
    #Slope = UnitUtils.ConvertToInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
    Getcondination =  Getintersection (Gird1.Curve,Gird2.Curve)
    LIST =  GetHt_Hn1 (ElementInstance,Slope,Plate_Column)
    Slope = UnitUtils.ConvertToInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
    H_t = LIST[1]
    H_n = LIST[0]
    with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                DataFromCSV_DATA = DataFromCSV(int(row[0]),None,None,None,None,None,Rafter_Type_Lefted,None,Length_Rafter,None,path,None,None,None,None,None,None,None)
                arr = DataFromCSV_DATA.Getcontentdata()
                Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t)
                Length_From_Gird =  arr[16]
                SumLength = DataFromCSV_DATA.checkLengthOfItemRafter()
                #SumLength_Inline = DataFromCSV_DATA.
                #Arr_Point_Type_Length=[Point_Level,arr[6],arr[8],arr[9]]
                Length_Rafter = arr[8]
                if Length_Rafter =="BAL":
                    #Length_Rafter = Length_From_Gird - float(SumLength) 
                    #print ("Length_From_Gird",Length_From_Gird, "SumLength is",SumLength )
                    #Length_Rafter1 = Length_From_Gird - float(SumLength)
                    Length_Rafter1 = ConvertToInternalUnitsmm(Length_From_Gird - float(SumLength))
                   #print ("Length_From_Gird",Length_From_Gird, "SumLength is",SumLength )

                    #Length_Rafter1 = UnitUtils.Convert(Length_From_Gird - float(SumLength) ,DisplayUnitType.DUT_MILLIMETERS, DisplayUnitType.DUT_DECIMAL_FEET)
            
                else:
                    #Length_Rafter1=Length_Rafter
                    Length_Rafter1 = ConvertToInternalUnitsmm(Length_Rafter)
                #Length_Rafter1 = UnitUtils.Convert(Length_Rafter,DisplayUnitType.DUT_MILLIMETERS, DisplayUnitType.DUT_DECIMAL_FEET)
                #Thinkess_Plate1 = UnitUtils.ConvertToInternalUnits(float(arr[9]), DisplayUnitType.DUT_MILLIMETERS)\
                Arr_Point_Type_Length=[Point_Level,arr[6],Length_Rafter1,arr[9]]
                Thinkess_Plate1 = ConvertToInternalUnitsmm(arr[9])

                #print ("length rapter is 1",Length_Rafter1)

                """
                H_n = H_n + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.cos(Slope) 
                H_t = H_t + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.sin(Slope)
                """
                GetHt_Hn = GetHt_HnTotal(arr[6], Length_Rafter1,Thinkess_Plate1,Slope,H_n,H_t)
                H_n = GetHt_Hn[0]
                H_t = GetHt_Hn[1]
                ArrTotal.append(Arr_Point_Type_Length)
            return ArrTotal
    csvFile.close()
def GetHt_HnTotal (ElementType, Length_Rafter,Thinkess_Plate1,Slope,H_n,H_t):
    FamilyRafterName = ElementType.FamilyName 
 
    if "4111b" in FamilyRafterName:
        H_n = H_n + Length_Rafter * math.cos(Slope)  + Thinkess_Plate1 * 2 
        H_t = H_t + Length_Rafter* math.sin(Slope) + Thinkess_Plate1 * 2 * math.tan(Slope)
      
    else:
        H_n = H_n + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.cos(Slope) 
        H_t = H_t + (Length_Rafter + Thinkess_Plate1 * 2 ) * math.sin(Slope)
    return [H_n,H_t]
def GetHt_Hn1 (ElementInstance,Slope,Plate_Column):

    Slope = UnitUtils.ConvertToInternalUnits(Slope, DisplayUnitType.DUT_DECIMAL_DEGREES)
    Plate_Column  = ConvertToInternalUnitsmm (Plate_Column)
    #print ("Plate_Column",Plate_Column)
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
    #print ("X_Left_X",X_Left_X,"X_Right_X",X_Right_X,"X_Top_X",X_Top_X,"X_Bottom_X",X_Bottom_X)
    return [h_n - X_Left_X + X_Right_X,h_t]
def setparameterfromvalue (elemeninstance,ValueName,setvalue):
    Tw2_Rafter = elemeninstance.LookupParameter(ValueName)
    Tw2_Rafter.Set(setvalue)
class DataFromCSV:
    def  __init__(self, Count, FamilyCol, FamilyColType,Base_Level_Col,Top_Level_Col,FamilyRafter,FamilyRafterType,LevelRafter,Length_Rafter,\
        Thinkess_Plate,path,Gird1,Gird2,Slope,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Gird,Plate_Column):
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
        self.Plate_Column = Plate_Column

    def writefilecsv(self,a,workbook):
        #row = [str(self.Count), str(self.FamilyRafterType.Id), self.FamilyRafterType.Id,str(self.Length_Rafter) ]
        row_Str = [self.Count, self.FamilyCol.Name,  Element.Name.__get__(self.FamilyColType),self.Base_Level_Col.Name,self.Top_Level_Col.Name,\
            self.FamilyRafter.Name, Element.Name.__get__(self.FamilyRafterType),self.LevelRafter.Name,self.Length_Rafter,\
                self.Thinkess_Plate,self.path,self.Gird1.Name,self.Gird2.Name,self.Slope,self.Gird_Ver_Ged.Name,self.Gird_Hor_Ged.Name,self.Length_From_Gird,self.Plate_Column]
        #workbook = ex.Workbooks.Open(path_excel)
        ws_Sheet1 = workbook.Worksheets[1]
        a = a + 2
        i = 1 
        for item in row_Str:
            ws_Sheet1.Cells(a,i).Value2 = str(item)
            i =i+1
        workbook.Save()
        workbook.Close()
    def GetContentDataFromExcel(self,path_excel):
        workbook = ex.Workbooks.Open(path_excel)
        ws_Sheet1 = workbook.Worksheets[1]
        #wb = xlrd.open_workbook(path_excel1)
        #ws_Sheet1 = workbook.Worksheets[1]
        sheet = wb.sheet_by_index(0)
        print("ws_Sheet1",sheet)
        for i in range (18):
            Element = ws_Sheet1.Cells(int(self.Count),int(i)).Value
            Element = sheet.cell_value(int(self.Count), i) 
            ArrData = GetElementByName(str(i),Element)
            GetContentDataFromExcelArr.append(ArrData) 
        #print ("GetContentDataFromExcelArr is",GetContentDataFromExcelArr)
        return GetContentDataFromExcelArr
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
                    Row8 = CheckTypeLengthBal(row[8])
                    Length_Rater_Lefted_n = Row8
                    Thinkess_Plate = float (row[9])
                    Gird1 = doc.GetElement(ElementId(int(row[11])))
                    Gird2 = doc.GetElement(ElementId(int(row[12])))
                    Slope = float (row[13])
                    Gird_Ver_G = doc.GetElement(ElementId(int(row[14])))
                    Gird_Hor_G = doc.GetElement(ElementId(int(row[15])))
                    Length_From_Gird = float (row[16])
                    Plate_Column = float(row[17])
                    arr = [self.Count, Column_Left, FamilyColType,Base_Level_Col,Top_Level_Col,Rafter_Family_Lefted,\
                        Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Thinkess_Plate,self.path,Gird1,Gird2,Slope,\
                            Gird_Ver_G,Gird_Hor_G,Length_From_Gird,Plate_Column]
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
                            str(self.Gird_Hor_Ged.Id),str(self.Length_From_Gird),str(self.Plate_Column)]
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

        Base_Leveled_Point =XYZ (Getcondination.X - X_Left_X +X_Right_X  ,Getcondination.Y,(LEVEL_ELEV_Base_Level + X_Top_X - X_Bottom_X))

        ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, self.FamilyColType,self.Base_Level_Col, Structure.StructuralType.NonStructural)
        #LIST = GetParameterFromSubElement(ColumnCreate,self.Slope)
        a= Global(self.Slope,None,None)
        a.globalparameterchange(ColumnCreate)
        a = Global(self.Plate_Column,"Pl_Rafter",ColumnCreate)
        a.SetParameterInstance()
        paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLeve.Set(self.Top_Level_Col.Id)
        TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
        TopoffsetPam.Set(0)
        #t.Commit()
        return ColumnCreate
    def PlaceElementRafterFather(self,ColumnCreate):
        #GetParameterFromSubElement (ElementInstance,Rafter_Type_Lefted,Slope,Length_Rafter,path,Gird1,Gird2):
        Point_Levels = GetParameterFromSubElement (ColumnCreate,self.FamilyRafterType,self.Slope,self.Length_Rafter,self.path,self.Gird1,self.Gird2,self.Thinkess_Plate,self.Plate_Column)
        for Point_Level,FamilyRafterType,Length_Rafter, Thinkess_Plate in Point_Levels:
            #Length_Rafter = UnitUtils.ConvertToInternalUnits(float(Length_Rafter), DisplayUnitType.DUT_MILLIMETERS)
            PlaceElementRafter(Point_Level,FamilyRafterType,self.LevelRafter,Length_Rafter,self.Slope,float(Thinkess_Plate))
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
                if row[8] == "BAL":
                    continue
                else:
                    sum = sum + float(row[8]) 
        csvFile.close()
        return sum
    def GetSumLengthAndPlate(self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            Sum_Length = 0 
            Sum_Plate = 0 
            for row in readcsv:
                if row[8] == "BAL":
                    continue
                else:
                    Sum_Length = Sum_Length + float(row[8]) 
            for row in readcsv:
                Sum_Plate = Sum_Plate +  float (row[9])
        csvFile.close()
        return Sum_Length + Sum_Plate

def PlaceElementRafter (Point_Level,Rater_Type_Lefted,Level_Rater_Type_Lefted,Length_Rater_Lefted,Slope_Type,Thinkess_Plate):
    if Rater_Type_Lefted.IsActive == False:
	    Rater_Type_Lefted.Activate()
	    doc.Regenerate()
    Elementinstance = doc.Create.NewFamilyInstance(Point_Level,Rater_Type_Lefted, Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)
    a= Global(Slope_Type,None,None)
    a.globalparameterchange(Elementinstance)
    a= Global(Thinkess_Plate,"Pl_Right",Elementinstance)
    a.SetParameterInstance()
    setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
def Getintersection (line1, line2):
    results = clr.Reference[IntersectionResultArray]()
    result = line1.Intersect(line2, results)
    if result != SetComparisonResult.Overlap:
	    print('No Intesection, Review Gird was chose')
    res = results.Item[0]
    return res.XYZPoint
def CheckTypeLengthBal(Length_Rater):
    if  Length_Rater == "BAL":
        Length = "BAL"
    else:
        Length = float(Length_Rater)
    return Length
def GetElementByName(Count, NameElement):
    #print ("Count",Count)
    if any(str(Count) in s for s in [str(1),str(5)]):
        for vt in FilteredElementCollector(doc).OfClass(Family):
            if vt.Name == NameElement:
               vt_Element = vt 
               return vt_Element  
    elif  any(Count in s for s in [str(2),str(6)]):
        for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements():
            if Element.Name.__get__(vt)  == NameElement:
                vt_Element = vt
                return vt_Element  
    elif any(Count in s for s in [str(3),str(4),str(7)]):
        for vt in FilteredElementCollector(doc).OfClass(Level):
            vt_Element = vt
            return vt_Element  
    elif any(Count in s for s in [str(11),str(12),str(14),str(15)]):
        for vt in FilteredElementCollector(doc).OfClass(Grid):
            vt_Element = vt
            return vt_Element  
    else:
        vt_Element =  NameElement
        return vt_Element  

"""
    for vt in FilteredElementCollector(doc).OfClass(Family):
        if vt.Name == NameElement:
            k =1
            vt_Element = vt
            return vt_Element   
    for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements():
        if Element.Name.__get__(vt)  == NameElement:
            k =2
            vt_Element = vt
            return vt_Element   
    for vt in FilteredElementCollector(doc).OfClass(Grid):
        if vt.Name == NameElement:
            k =3
            vt_Element = vt
            return vt_Element   
    for vt in FilteredElementCollector(doc).OfClass(Level):
        if vt.Name == NameElement:
            k =4
            vt_Element = vt
            return vt_Element   
    if result:
        vt_Element =  (NameElement)
        return vt_Element    

        [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.Name == str(NameElement)] !=None:

        #vt_Element = [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.Name == str(NameElement)]#
        
    elif [vt for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements() if Element.Name.__get__(vt) == str(NameElement)] != None:
        vt_Element = [vt for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements() if Element.Name.__get__(vt) == str(NameElement)]
    elif [vt for vt in FilteredElementCollector(doc).OfClass(Grid) if vt.Name == str(NameElement)] != None:
        vt_Element = [vt for vt in FilteredElementCollector(doc).OfClass(Grid) if vt.Name == str(NameElement)]
    elif [vt for vt in FilteredElementCollector(doc).OfClass(Grid) if vt.Name == str(NameElement)] != None:
        vt_Element = [vt for vt in FilteredElementCollector(doc).OfClass(Level) if vt.Name == str(NameElement)]
    else:
        vt_Element = str (NameElement)
    print (vt_Element)
    return vt_Element


WORKSHEET_NAME = "Sheet1"
class ExcelInstance():
    def __init__(self, wb=None):
        self.source_path = path_excel
        try:
            self.app = win32com.client.gencache.EnsureDispatch('Excel.Application')
        except:
            print("Application could not be opened.")
            return
        try:
            self.open_workbook()
        except:
            print("Workbook could not be opened.")
            return
        try:
            self.ws = self.wb.Worksheets(WORKSHEET_NAME) 
        except:
            print("Worksheet not found.")
            return
        self.app.Visible = True
        self.app.WindowState = win32com.client.constants.xlMaximized

    def open_workbook(self):
        
        If it doesn't open one way, try another.
        
        try:        
            self.wb = self.app.Workbooks(self.source_path)            
        except Exception as e:
            try:
                self.wb = self.app.Workbooks.Open(self.source_path)
            except Exception as e:
                print(e)
                self.wb = None   

    def get_column_after(self, column, offset):
        for item in self.ws.Range("{0}{1}:{0}{2}".format(column, offset, self.get_last_row_from_column(column))).Value:
            print(item[0])

    def get_last_row_from_column(self, column):
        return self.ws.Range("{0}{1}".format(column, self.ws.Rows.Count)).End(win32com.client.constants.xlUp).Row
"""
