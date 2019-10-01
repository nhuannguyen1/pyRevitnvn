from Autodesk.Revit.DB import Transaction,Element, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId, Element
from Autodesk.Revit.DB.UnitUtils import ConvertFromInternalUnits
import rpw
import csv
import clr
import Csv_Connect_Data
from Csv_Connect_Data import DataCSV
import FamilySymbol
from ConvertAndCaculation import Global,ConvertToInternalUnits,ConvertToInternalUnitsmm,setparameterfromvalue,GetCondinationH_nAndH_V,GetCoordinateContinnue
import CreateMiddlemenElement
from System.Collections.Generic import List
# import the Excel Interop. 
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import math 
DataToolTemplate = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\DataToolTemplate.csv"
DataFromCsv  = DataCSV (DataToolTemplate)
def GetPath ():
    return DataToolTemplate
def ArrFistForDefautValue_FC():
    Arr = DataFromCsv.ArrFistForDefautValue()
    return Arr
def CountNumberOfRow():
    L_Row = DataFromCsv.CountNumberOfRow()
    return L_Row
def CountNumberOfColumn():
    L_Column = DataFromCsv.CountNumberOfColumn()
    return L_Column
def writeRowTitle():
    DataFromCsv.writeRowTitle()
class DataFromCSV:
    def  __init__(self, *List):
        self.Count = List[0]
        self.FamilyCol = List[1]
        self.FamilyColType =  List[2]
        self.Base_Level_Col =  List[3]
        self.Top_Level_Col =  List[4]
        self.FamilyRafter =  List[5]
        self.FamilyRafterType =  List[6]
        self.LevelRafter = List[7]
        self.Length_Rafter = List[8]
        self.Thinkess_Plate = List[9]
        self.path = List[10] 
        self.Gird_Ver = List[11]
        self.Gird_hor = List[12]
        self.Slope = List[13]
        self.Gird_Ver_Ged = List[14]
        self.Gird_Hor_Ged = List[15]
        self.Length_From_Gird = List[16]
        self.Plate_Column = List[17]
        self.Move_Left =  List[18]
        self.Move_Right =  List[19]
        self.Move_Up = List[20]
        self.Move_Bottom = List[21]
        self.Offset_Top_Level = List[22]
    def ArrDataList(self):
        ArrDataList = [self.Count,self.FamilyCol, self.FamilyColType ,self.Base_Level_Col,\
            self.Top_Level_Col,self.FamilyRafter,self.FamilyRafterType,self.LevelRafter,\
                self.Length_Rafter, self.Thinkess_Plate,self.path,self.Gird_Ver,self.Gird_hor,self.Slope,\
                    self.Gird_Ver_Ged,self.Gird_Hor_Ged, self.Length_From_Gird,self.Plate_Column,\
                        self.Move_Left,self.Move_Right, self.Move_Up,self.Move_Bottom,self.Offset_Top_Level]
        return ArrDataList
    def writefileExcel(self,a):
        #DataExcel1 = DataExcel(self.path, "Sheet1")
        row_Str = [CheckSelectedValueForFamily(vt) for vt in self.ArrDataList()]    
        DataFromCsv.writefilecsvFromRowArr(row_Str)
    def GetContentDataFromExcel(self):
        a = self.Count
        ArrGetContentData = DataFromCsv.GetContentDataByName(a)
        return ArrGetContentData
    def GetContentDataFromExcel_Test2(self):
        a = self.Count + 1
        ArrGetContentData = DataFromCsv.GetContentDataByName(a)
        return ArrGetContentData
    def GetContentDataFromExcel_Test(self):
        a = self.Count - 1
        ArrGetContentData = DataFromCsv.GetContentDataByName(a)
        #print ("ArrGetContentData",ArrGetContentData)
        return ArrGetContentData
    def Return_Row_Excel (self):
        row_Str = [CheckSelectedValueForFamily(vt) for vt in self.ArrDataList()]
        return row_Str
    def InputDataChangeToCSV_Excel(self,row_input):
        DataFromCsv.InputDataChangeToCSV(self.Count,row_input)
    def PlaceElement (self):
        #self.Length_Rafter = (UnitUtils.ConvertToInternalUnits(float(self.Length_Rafter), DisplayUnitType.DUT_MILLIMETERS))
        self.Move_Up  = ConvertToInternalUnitsmm (self.Move_Up)
        self.Move_Bottom  = ConvertToInternalUnitsmm (self.Move_Bottom)
        self.Move_Left  = ConvertToInternalUnitsmm (self.Move_Left)
        self.Move_Right  = ConvertToInternalUnitsmm (self.Move_Right)
        LEVEL_ELEV_Base_Level= self.Top_Level_Col.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        Getcondination =  Getintersection (self.Gird_Ver.Curve,self.Gird_hor.Curve)
        Base_Leveled_Point =XYZ (Getcondination.X - self.Move_Left + self.Move_Right ,\
            Getcondination.Y,(LEVEL_ELEV_Base_Level + self.Move_Up - self.Move_Bottom))
        FamilySymbol.FamilySymbolAtive(self.FamilyColType)
        t = Transaction (doc,"Place Element 1")
        t.Start()
        ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, self.FamilyColType,\
            self.Base_Level_Col, Structure.StructuralType.NonStructural)
        #LIST = GetParameterFromSubElement(ColumnCreate,self.Slope)
        Global1= Global(self.Slope,None,None)
        Global1.globalparameterchange(ColumnCreate)
        a = Global(self.Plate_Column,"Pl_Rafter",ColumnCreate)
        a.SetParameterInstance()
        SetTopLevel = Global(self.Offset_Top_Level,"Top Offset",ColumnCreate)
        SetTopLevel.SetParameterInstance()
        paramerTopLevel = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLevel.Set(self.Top_Level_Col.Id)
        #TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
        #TopoffsetPam.Set(0)
        t.Commit()
        return ColumnCreate
    def CreateElement(self):
        ColumnCreate = self.PlaceElement()
        RaffterElment = self.PlaceElementRafterFather(ColumnCreate)
        RaffterElment.Add(ColumnCreate.Id)
        t = Transaction (doc,"Place Element 3")
        t.Start()
        Getcondination =  Getintersection (self.Gird_Ver.Curve,self.Gird_hor.Curve)
        CreateMiddlemenElement.CreateElementByMirror(RaffterElment,Getcondination,self.Length_From_Gird)
        t.Commit()
    def PlaceElementRafterFather(self,ColumnCreate):
        ArrPlaceElementRafterFather = List[ElementId]()
        t = Transaction (doc,"Place Element 2")
        t.Start()
        Point_Levels = self.GetParameterFromSubElement (ColumnCreate)
        for Point_Level,FamilyRafterType,Length_Rafter, Thinkess_Plate in Point_Levels:
            PlaceElementRafter_FN = PlaceElementRafter(Point_Level,FamilyRafterType,self.LevelRafter,Length_Rafter,self.Slope,float(Thinkess_Plate))
            ArrPlaceElementRafterFather.Add(PlaceElementRafter_FN.Id)
        t.Commit()
        return ArrPlaceElementRafterFather
    def LengthToTotalInlineFromGird (self,Length_From_Gird):
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        LineInline = (Length_From_Gird)/ (math.cos(Slope))
        return LineInline
    def GetParameterFromSubElement (self,ElementInstance):
        lr_Row = CountNumberOfRow()
        Arr_Point_Type_Length = []
        ArrTotal = []
        Getcondination =  Getintersection (self.Gird_Ver.Curve,self.Gird_hor.Curve)
        LIST =  GetCondinationH_nAndH_V (ElementInstance,self.Slope,self.Plate_Column,self.Move_Left,self.Move_Right,self.Offset_Top_Level)
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        H_t = LIST[1]
        H_n = LIST[0]
        Length_From_Gird_T = ConvertToInternalUnitsmm(float (self.Length_From_Gird)) - H_n
        #Length_From_Gird_Dis = ConvertFromInternalUnits(float(Length_From_Gird_T),DisplayUnitType.DUT_MILLIMETERS)
        Length_From_Gird = self.LengthToTotalInlineFromGird(Length_From_Gird_T)
        for i in range(1,int(lr_Row)):
            ArrFistForDefautValue = ArrFistForDefautValue_FC()
            ArrFistForDefautValue[0] = i 
            ArrFistForDefautValue [10] = self.path
            DataFromCSV_DATA = DataFromCSV(*ArrFistForDefautValue)
            arr = DataFromCSV_DATA.GetContentDataFromExcel()
            Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t)
            SumLength = DataFromCsv.checkLengthAngGetSumOfItemRafterFromCsv(lr_Row)
            Length_Rafter = arr[8]
            if Length_Rafter =="BAL":
                Length_Rafter = (Length_From_Gird - ConvertToInternalUnitsmm(float(SumLength)))
                if Length_Rafter < 0:
                    print ("check length again ")
            else:
                Length_Rafter = ConvertToInternalUnitsmm(Length_Rafter)
            Arr_Point_Type_Length=[Point_Level,arr[6],Length_Rafter,arr[9]]
            Thinkess_Plate1 = ConvertToInternalUnitsmm(arr[9])
            #print ("arr[6] is ",arr[6])
            GetHt_Hn = GetCoordinateContinnue(arr[6], Length_Rafter,Thinkess_Plate1,Slope,H_n,H_t)
            H_n = GetHt_Hn[0]
            H_t = GetHt_Hn[1]
            ArrTotal.append(Arr_Point_Type_Length)
        return ArrTotal
    def DeleteRowToReset(self):
        DataFromCsv.DeleteRow(self.Count)
def PlaceElementRafter (Point_Level,Rater_Type_Lefted,Level_Rater_Type_Lefted,Length_Rater_Lefted,Slope_Type,Thinkess_Plate):
    FamilySymbol.FamilySymbolAtive(Rater_Type_Lefted)
    Elementinstance = doc.Create.NewFamilyInstance(Point_Level,Rater_Type_Lefted, Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)
    a= Global(Slope_Type,None,None)
    a.globalparameterchange(Elementinstance)
    #print ("Elementinstance is",Elementinstance.Name )
    a= Global(Thinkess_Plate,"Pl_Right",Elementinstance)
    a.SetParameterInstance()
    setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
    return Elementinstance
def Getintersection (line1, line2):
    results = clr.Reference[IntersectionResultArray]()
    result = line1.Intersect(line2, results)
    if result != SetComparisonResult.Overlap:
	    print('No Intesection, Review Gird was choise')
    res = results.Item[0]
    return res.XYZPoint
def CheckTypeLengthBal(Length_Rater):
    if  Length_Rater == "BAL":
        Length = "BAL"
    else:
        Length = float(Length_Rater)
    return Length
def CheckSelectedValueForFamily(SelectedValue):
    if SelectedValue == None:
        return None
    else:
        try:
            SelectedValue1 = SelectedValue.Name
            return SelectedValue1
        except:
                try:
                    SelectedValue1 = Element.Name.__get__(SelectedValue)
                    return SelectedValue1
                except:
                    try:
                        if(type (SelectedValue) is str) or (type (SelectedValue) is float) or (type (SelectedValue) is int) :
                            SelectedValue1 = str(SelectedValue)
                            return SelectedValue1
                    except:
                        pass
def ArrDataExcell1(Col):
    ArrDataExcell = []
    for i in range (0,Col):
        ArrDataExcell.append(None)
        i +=1
    return ArrDataExcell