from Autodesk.Revit.DB import Transaction,Element, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId, Element
from Autodesk.Revit.DB.UnitUtils import ConvertFromInternalUnits
import rpw
import csv
import clr
import Csv_Connect_Data
from Csv_Connect_Data import DataCSV,SaveDataToCSV
import FamilySymbol
from ConvertAndCaculation import Global,ConvertToInternalUnits,ConvertToInternalUnitsmm,setparameterfromvalue,GetCondinationH_nAndH_V,GetCoordinateContinnue
import CreateMiddlemenElement
import CheckAndChoice
from System.Collections.Generic import List
# import the Excel Interop. 
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import math 
import DirectoryPath
from DirectoryPath import Path_Config_Setting
ArrPath = DirectoryPath.ReturnPath()
Genneral_Parameter =ArrPath[0]
Left_DataSaveToCaculation = ArrPath[1]
Left_Member_Change = ArrPath[2]
Left_Member_Change_U = ArrPath[3]
Right_DataSaveToCaculation = ArrPath[4]
Right_Member_Change = ArrPath[5]
Right_Member_Change_U = ArrPath[6]
Left_Member_All = ArrPath[7]
Right_Member_All = ArrPath[8]
SaveDataToCSV = SaveDataToCSV(Left_DataSaveToCaculation)
def GetPath_Genneral_Parameter():
    return Genneral_Parameter
def GetPath_Left_DataSaveToCaculation ():
    return Left_DataSaveToCaculation
def GetPath_Left_Member_Change ():
    return Left_Member_Change
def GetPath_Left_Member_Change_U ():
    return Left_Member_Change_U
def GetPath_Right_DataSaveToCaculation ():
    return Right_DataSaveToCaculation
def GetPath_Right_Member_Change ():
    return Right_Member_Change
def GetPath_Right_Member_Change_U():
    return Right_Member_Change_U
def GetPath_Left_Member_All():
    return Left_Member_All
def GetPath_Right_Member_All():
    return Right_Member_All
def ArrFistForDefautValue_FC(path):
    DataFromCsv_New  = DataCSV (path)
    Arr = DataFromCsv_New.ArrFistForDefautValue()
    return Arr
def CountNumberOfRow(path):
    DataFromCsv_New  = DataCSV (path)
    L_Row = DataFromCsv_New.CountNumberOfRow()
    return L_Row
def CountNumberOfColumn(path):
    DataFromCsv_New  = DataCSV (path)
    L_Column = DataFromCsv_New.CountNumberOfColumn()
    return L_Column
def writeRowTitle(path):
    DataFromCsv  = DataCSV (path)
    DataFromCsv.writeRowTitle(Path_Config_Setting)
def SynChronizeValueToCSV_T(path):
    DataFromCsv_New  = DataCSV (path)
    DataFromCsv_New.SynChronizeValueToCSV(Path_Config_Setting)

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
    def writefileExcel(self,a,CheckPath):
        if CheckPath ==Left_Member_All:
            Path_Member_Change_U = Left_Member_Change_U
            Path_Member_Change = Left_Member_Change
        elif CheckPath ==Right_Member_All:
            Path_Member_Change_U = Right_Member_Change_U
            Path_Member_Change = Right_Member_Change
        else:
            pass
        row_Str = [CheckSelectedValueForFamily(vt) for vt in self.ArrDataList()]    
        DataFromCsv  = DataCSV (CheckPath)
        DataFromCsv.writefilecsvFromRowArr(row_Str)
    def GetContentDataFromExcel(self,path,index):
        a = self.Count + index
        DataFromCsv_New  = DataCSV(path)
        ArrGetContentData = DataFromCsv_New.GetContentDataByName(a)
        return ArrGetContentData
    def Return_Row (self):
        row_Str = [CheckSelectedValueForFamily(vt) for vt in self.ArrDataList()]
        return row_Str
    def InputDataChangeToCSV_Excel(self,row_input,path):
        DataFromCsv_New  = DataCSV(path)
        DataFromCsv_New.InputDataChangeToCSV(self.Count,row_input)
    def PlaceElement (self):
        self.Move_Up  = ConvertToInternalUnitsmm (self.Move_Up)
        self.Move_Bottom  = ConvertToInternalUnitsmm (self.Move_Bottom)
        self.Move_Left  = ConvertToInternalUnitsmm (self.Move_Left)
        self.Move_Right  = ConvertToInternalUnitsmm (self.Move_Right)
        LEVEL_ELEV_Base_Level= self.Top_Level_Col.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        Getcondination =  Getintersection(self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path)
        Base_Leveled_Point =XYZ (Getcondination.X - self.Move_Left + self.Move_Right ,\
            Getcondination.Y,(LEVEL_ELEV_Base_Level + self.Move_Up - self.Move_Bottom))
        FamilySymbol.FamilySymbolAtive(self.FamilyColType)
        t = Transaction (doc,"Place Element 1")
        t.Start()
        ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, self.FamilyColType,\
            self.Base_Level_Col, Structure.StructuralType.NonStructural)
        NameParameter = CheckAndChoice.GetParameterName(self.path)
        Global1= Global(self.Slope,NameParameter,ColumnCreate)
        Global1.globalparameterchange()
        a = Global(self.Plate_Column,"Pl_Rafter",ColumnCreate)
        a.SetParameterInstance()
        SetTopLevel = Global(self.Offset_Top_Level,"Top Offset",ColumnCreate)
        SetTopLevel.SetParameterInstance()
        paramerTopLevel = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLevel.Set(self.Top_Level_Col.Id)
        t.Commit()
        return ColumnCreate
    def CreateElement(self):
        ColumnCreate = self.PlaceElement()
        RaffterElment = self.PlaceElementRafterFather(ColumnCreate)
        RaffterElment.Add(ColumnCreate.Id)
        Getcondination =  Getintersection (self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path)
        return [RaffterElment,Getcondination,self.Length_From_Gird] 
    def PlaceElementRafterFather(self,ColumnCreate):
        ArrPlaceElementRafterFather = List[ElementId]()
        t = Transaction (doc,"Place Element 2")
        t.Start()
        Point_Levels = self.GetParameterFromSubElement (ColumnCreate)
        for Point_Level,FamilyRafterType,Length_Rafter, Thinkess_Plate in Point_Levels:
            PlaceElementRafter_FN = PlaceElementRafter(Point_Level,FamilyRafterType,self.LevelRafter,Length_Rafter,self.Slope,float(Thinkess_Plate),self.path)
            ArrPlaceElementRafterFather.Add(PlaceElementRafter_FN.Id)
        t.Commit()
        return ArrPlaceElementRafterFather
    def LengthToTotalInlineFromGird (self,Length_From_Gird):
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        LineInline = (Length_From_Gird)/ (math.cos(Slope))
        return LineInline
    def GetParameterFromSubElement (self,ElementInstance):
        lr_Row = CountNumberOfRow(self.path)
        Arr_Point_Type_Length = []
        ArrTotal = []
        Getcondination =  Getintersection (self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path)
        LIST =  GetCondinationH_nAndH_V (ElementInstance,self.Slope,self.Plate_Column,self.Move_Left,self.Move_Right,self.Offset_Top_Level)
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        H_t = LIST[1]
        H_n = LIST[0]
        Length_From_Gird_T = ConvertToInternalUnitsmm(float (self.Length_From_Gird)) - H_n
        #Length_From_Gird_Dis = ConvertFromInternalUnits(float(Length_From_Gird_T),DisplayUnitType.DUT_MILLIMETERS)
        Length_From_Gird = self.LengthToTotalInlineFromGird(Length_From_Gird_T)
        for i in range(1,int(lr_Row)):
            ArrFistForDefautValue = ArrFistForDefautValue_FC(self.path )
            ArrFistForDefautValue[0] = i 
            ArrFistForDefautValue [10] = self.path
            DataFromCSV_DATA = DataFromCSV(*ArrFistForDefautValue)
            arr = DataFromCSV_DATA.GetContentDataFromExcel(self.path,0)
            Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t)
            DataFromCsv_New  = DataCSV(self.path)
            SumLength = DataFromCsv_New.checkLengthAngGetSumOfItemRafterFromCsv(lr_Row)
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
        #print ("(H_n,H_t)",H_n,H_t)
        SaveDataToCSV.SaveDataH_tAndH_N(H_n,H_t)
        return ArrTotal
    def DeleteRowToReset(self,path):
        DataFromCsv_New  = DataCSV(path)
        DataFromCsv_New.DeleteRow(self.Count)
    def Set_Count (self,CountNew):
        self.Count = CountNew
    def SetPath (self,path):
        self.path = path
def PlaceElementRafter (Point_Level,Rater_Type_Lefted,Level_Rater_Type_Lefted,Length_Rater_Lefted,Slope_Type,Thinkess_Plate,path):
    FamilySymbol.FamilySymbolAtive(Rater_Type_Lefted)
    Elementinstance = doc.Create.NewFamilyInstance(Point_Level,Rater_Type_Lefted, Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)
    #RowValue = PathTemplate.ReturnDataAllRowByIndex(3)
    NameParameter = CheckAndChoice.GetParameterName(path)
    a= Global(Slope_Type,NameParameter,Elementinstance)
    a.globalparameterchange()
    #print ("Elementinstance is",Elementinstance.Name )
    a= Global(Thinkess_Plate,"Pl_Right",Elementinstance)
    a.SetParameterInstance()
    setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
    return Elementinstance
def Getintersection (line1, line2,line3,line4,path ):
    if path == Right_Member_All:
        line1 = line3
        line2 = line4
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
def SetValueForARR(Arr1,Arr2):
    for i in range (0,len(Arr1)-1):
        Arr1[i] = Arr2[1]