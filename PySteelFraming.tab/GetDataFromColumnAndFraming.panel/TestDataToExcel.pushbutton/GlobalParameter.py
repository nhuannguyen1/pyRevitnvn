from Autodesk.Revit.DB import Transaction,Element, FilteredElementCollector,\
    BuiltInCategory,FamilySymbol,XYZ,Structure,Family,Level,\
    BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,\
    UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue,ElementId, Element,Curve
import rpw
import csv
from Csv_Steel.Csv_Connect_Data import DataCSV,SaveDataToCSV
import FamilySymbol
from ConvertAndCaculation import Global,ConvertToInternalUnits,ConvertToInternalUnitsmm,\
    setparameterfromvalue,CaculateForFraming,\
        ConvertFromInteralUnitToMM,GetParamaterFromElementType
import CheckAndChoice
from System.Collections.Generic import List
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
import math 
from  PySteelFraming.GetElementByName import ElementName
from  PySteelFraming.SteelPath import PathSteel
from  Line_Steel.Line_Steel import LineInterSection
class DataFromCSV:
    def  __init__(self, Count = 1,FamilyCol = None,FamilyColType = None,Base_Level_Col= None,Top_Level_Col = None,\
        FamilyRafter= None,FamilyRafterType = None,LevelRafter = None,Length_Rafter = None,Thinkess_Plate = None, path = None,Gird_Ver=None,Gird_hor = None,\
            Slope = None,Gird_Ver_Ged = None,Gird_Hor_Ged = None,Length_From_Gird = None, Plate_Column = None,Move_Left = None, Move_Right = None,\
                Move_Up = None,Move_Bottom = None, Offset_Top_Level  = None, Select_Level = None,Clear_Height = None, Peak_Height = None, Eave_Height = None,\
                    Choose_Purlin = None,Choose_Type_Purlin= None, Path_Config_Setting = None,Right_Member_All = None,Left_DataSaveToCaculation = None):
        
        self.Count = Count
        self.FamilyCol = FamilyCol
        self.FamilyColType =  FamilyColType
        self.Base_Level_Col =  Base_Level_Col
        self.Top_Level_Col =  Top_Level_Col
        self.FamilyRafter =  FamilyRafter
        self.FamilyRafterType = FamilyRafterType
        self.LevelRafter = LevelRafter
        self.Length_Rafter = Length_Rafter
        self.Thinkess_Plate = Thinkess_Plate
        self.path =path
        self.Gird_Ver = Gird_Ver
        self.Gird_hor = Gird_hor
        self.Slope = Slope
        self.Gird_Ver_Ged =Gird_Ver_Ged
        self.Gird_Hor_Ged = Gird_Hor_Ged
        self.Length_From_Gird = Length_From_Gird
        self.Plate_Column = Plate_Column
        self.Move_Left =  Move_Left
        self.Move_Right =  Move_Right
        self.Move_Up = Move_Up
        self.Move_Bottom = Move_Bottom
        self.Offset_Top_Level = Offset_Top_Level
        self.Select_Level = Select_Level
        self.Clear_Height = Clear_Height
        self.Peak_Height = Peak_Height
        self.Eave_Height = Eave_Height
        self.Choose_Purlin =Choose_Purlin
        self.Choose_Type_Purlin = Choose_Type_Purlin
        #not fill out to csv
        self.Path_Config_Setting = Path_Config_Setting
        self.Right_Member_All = Right_Member_All
        self.Left_DataSaveToCaculation = Left_DataSaveToCaculation
    def ArrDataList(self):
        ArrDataList = [self.Count,self.FamilyCol, self.FamilyColType ,self.Base_Level_Col,\
            self.Top_Level_Col,self.FamilyRafter,self.FamilyRafterType,self.LevelRafter,\
                self.Length_Rafter, self.Thinkess_Plate,self.path,self.Gird_Ver,self.Gird_hor,self.Slope,\
                    self.Gird_Ver_Ged,self.Gird_Hor_Ged, self.Length_From_Gird,self.Plate_Column,\
                        self.Move_Left,self.Move_Right, self.Move_Up,self.Move_Bottom,\
                            self.Offset_Top_Level,self.Select_Level,self.Clear_Height,\
                                self.Peak_Height,self.Eave_Height,self.Choose_Purlin,self.Choose_Type_Purlin]
        return ArrDataList
    def writefileExcel(self,a,CheckPath):
        row_Str = [CheckSelectedValueForFamily(vt) for vt in self.ArrDataList()]    
        DataFromCsv  = DataCSV (CheckPath)
        DataFromCsv.writefilecsvFromRowArr(row_Str)
    def GetContentDataFromExcel(self,path,index):
        a = self.Count + index
        ArrGetContentData = GetContentDataByName(path,a,self.Path_Config_Setting)
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
        LineInterSection_HD = LineInterSection(self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path,self.Right_Member_All)
        Getcondination =  LineInterSection_HD.Getintersection()
        Base_Leveled_Point =XYZ (Getcondination.X - self.Move_Left + self.Move_Right ,\
            Getcondination.Y,(LEVEL_ELEV_Base_Level + self.Move_Up - self.Move_Bottom))
        FamilySymbol.FamilySymbolAtive(self.FamilyColType)
        t = Transaction (doc,"Place Element 1")
        t.Start()
        ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, self.FamilyColType,\
            self.Base_Level_Col, Structure.StructuralType.NonStructural)
        PathSteelHd = PathSteel (path = self.path, Path_Conf =self.Path_Config_Setting )
        NameParameter = PathSteelHd.GetParameterName()
        # check path and get distance from gird 
        LineInterSection_HD1 = LineInterSection(self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path,self.Right_Member_All)
        Distance = LineInterSection_HD1.GetDistanceRight (self.Length_From_Gird)

        self.SetLength_From_Gird (Distance)
        # Modify Slope, E.H
        Get_Parameter_D1_Of_Purlin = GetParamaterFromElementType(self.Choose_Type_Purlin,"D1")

        CheckChoice1 = CheckAndChoice.CheckChoice(path=self.path,Select_Level=self.Select_Level,\
            Clear_Height=self.Clear_Height,Peak_Height=self.Peak_Height,Eave_Height=self.Eave_Height,\
                Slope=self.Slope,Offset_Top_Level=self.Offset_Top_Level,Top_Level_Col=self.Top_Level_Col,\
                    ColumnCreate=ColumnCreate,X_Left=self.Move_Left,X_Right=self.Move_Right,Length_From_Gird=self.Length_From_Gird,\
                        Path_Config_Setting=self.Path_Config_Setting,LengthPurlin=Get_Parameter_D1_Of_Purlin)

        OfficeSetEH = CheckChoice1.GetSelectLevel()
        OfficeSetEH1 = ConvertFromInteralUnitToMM (OfficeSetEH[1])
        self.SetSlope(OfficeSetEH[0])
        self.SetOffsetColumn(str(- OfficeSetEH1))
        Global1= Global(self.Slope,NameParameter,ColumnCreate)
        Global1.globalparameterchange()
        a = Global(self.Plate_Column,"Pl_Rafter",ColumnCreate)
        a.SetParameterInstance()
        SetTopLevel = Global(- OfficeSetEH1,"Top Offset",ColumnCreate)
        SetTopLevel.SetParameterInstance()
        paramerTopLevel = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
        paramerTopLevel.Set(self.Top_Level_Col.Id)
        t.Commit()
        return ColumnCreate
    def CreateElement(self):
        ColumnCreate = self.PlaceElement()
        RaffterElment = self.PlaceElementRafterFather(ColumnCreate)
        RaffterElment.Add(ColumnCreate.Id)
        LineInterSection_HD = LineInterSection(self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path,self.Right_Member_All)
        Getcondination =  LineInterSection_HD.Getintersection ()
        return [RaffterElment,Getcondination,self.Length_From_Gird] 
    def PlaceElementRafterFather(self,ColumnCreate):
        ArrPlaceElementRafterFather = List[ElementId]()
        t = Transaction (doc,"Place Element 2")
        t.Start()
        Point_Levels = self.GetParameterFromSubElement (ColumnCreate)
        for Point_Level,FamilyRafterType,Length_Rafter, Thinkess_Plate in Point_Levels:
            PlaceElementRafter_FN = self.PlaceElementRafter(Point_Level,FamilyRafterType,self.LevelRafter,Length_Rafter,self.Slope,float(Thinkess_Plate),self.path)
            ArrPlaceElementRafterFather.Add(PlaceElementRafter_FN.Id)
        t.Commit()
        return ArrPlaceElementRafterFather
    def LengthToTotalInlineFromGird (self,Length_From_Gird):
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        LineInline = (Length_From_Gird)/ (math.cos(Slope))
        return LineInline
    def GetParameterFromSubElement (self,ElementInstance):
        DataCSV_HD = DataCSV(self.path)
        lr_Row = DataCSV_HD.CountNumberOfRow()
        Arr_Point_Type_Length = []
        ArrTotal = []
        LineInterSection_HD = LineInterSection(self.Gird_Ver.Curve,self.Gird_hor.Curve,self.Gird_Ver_Ged.Curve,self.Gird_Hor_Ged.Curve,self.path,self.Right_Member_All)
        Getcondination =  LineInterSection_HD.Getintersection ()
        CaculateForFramingHD = CaculateForFraming(ElementInstance =ElementInstance,Slope = self.Slope, Plate_Column= self.Plate_Column,\
             X_Left_X = self.Move_Left,X_Right_X= self.Move_Right,Offset_Top_Level = self.Offset_Top_Level)
        LIST =  CaculateForFramingHD.GetCondinationH_nAndH_V()
        Slope = UnitUtils.ConvertToInternalUnits(float(self.Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
        H_t = LIST[1]
        H_n = LIST[0]
        Length_From_Gird_T = ConvertToInternalUnitsmm(float (self.Length_From_Gird)) - H_n
        Length_From_Gird = self.LengthToTotalInlineFromGird(Length_From_Gird_T)
        for i in range(1,int(lr_Row)):
            DataFromCSV_DATA = DataFromCSV(Count= i,path=self.path,Path_Config_Setting= self.Path_Config_Setting)
            arr = DataFromCSV_DATA.GetContentDataFromExcel(self.path,0)
            #caculation Distance of rafter level anh column)
            H_t_Distance = (float(self.Top_Level_Col.Elevation) - float(self.LevelRafter.Elevation))

            Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t + H_t_Distance)
            SumLength = checkLengthAngGetSumOfItemRafterFromCsv(self.path,lr_Row)
            Length_Rafter = arr[8]
            if Length_Rafter =="BAL":
                Length_Rafter = (Length_From_Gird - ConvertToInternalUnitsmm(float(SumLength)))
                if Length_Rafter < 0:
                    print ("check length again ")
            else:
                Length_Rafter = ConvertToInternalUnitsmm(Length_Rafter)
            Arr_Point_Type_Length=[Point_Level,arr[6],Length_Rafter,arr[9]]
            Thinkess_Plate1 = ConvertToInternalUnitsmm(arr[9])
            CaculateForFramingHD = CaculateForFraming(ElementType=arr[6],Length_Rafter=Length_Rafter,Thinkess_Plate1=Thinkess_Plate1,Slope = Slope, Plate_Column= self.Plate_Column,\
             X_Left_X = self.Move_Left,X_Right_X= self.Move_Right,Offset_Top_Level = self.Offset_Top_Level,H_n=H_n,H_t=H_t)
            GetHt_Hn = CaculateForFramingHD.GetCoordinateContinnue()
            H_n = GetHt_Hn[0]
            H_t = GetHt_Hn[1]
            ArrTotal.append(Arr_Point_Type_Length)    
            ElevationCH = self.Top_Level_Col.Elevation
        SaveDataToCSV_hd = SaveDataToCSV (self.Left_DataSaveToCaculation)
        SaveDataToCSV_hd.SaveDataH_tAndH_N(H_n, float(H_t) + float (ElevationCH) )
        return ArrTotal
    def DeleteRowToReset(self,path):
        DataFromCsv_New  = DataCSV(path)
        DataFromCsv_New.DeleteRow(self.Count)
    def Set_Count (self,CountNew):
        self.Count = CountNew
    def SetOffsetColumn (self,Value):
        self.Offset_Top_Level = Value
    def SetPath (self,path):
        self.path = path
    def SetSlope (self,Slope):
        self.Slope = Slope
    def SetLength_From_Gird (self,Length_From_Gird):
        self.Length_From_Gird = Length_From_Gird
    def SetX_Left (self,Move_Left):
        self.Move_Left = Move_Left
    def SetX_Right (self,Move_Right):
        self.Move_Right = Move_Right
    def SynChronizeValueToCSV_T(self):
        DataFromCsv_New  = DataCSV (self.path)
        DataFromCsv_New.SynChronizeValueToCSV(self.Path_Config_Setting)
    def PlaceElementRafter (self,Point_Level,Rater_Type_Lefted,Level_Rater_Type_Lefted,Length_Rater_Lefted,Slope_Type,Thinkess_Plate,path):
        FamilySymbol.FamilySymbolAtive(Rater_Type_Lefted)
        Elementinstance = doc.Create.NewFamilyInstance(Point_Level,Rater_Type_Lefted, Level_Rater_Type_Lefted, Structure.StructuralType.NonStructural)

        PathSteelHd = PathSteel (path = self.path, Path_Conf =self.Path_Config_Setting )
        #NameParameter = PathSteelHd.GetParameterName()
        NameParameter = PathSteelHd.GetParameterName()
        a= Global(Slope_Type,NameParameter,Elementinstance)
        a.globalparameterchange()
        a= Global(Thinkess_Plate,"Pl_Right",Elementinstance)
        a.SetParameterInstance()
        setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
        return Elementinstance
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
def GetContentDataByName(path,Count,Path_Config_Setting):
    GetContentDataFromCsv = []
    with open(path) as csvFile:
        readcsv =csv.reader(csvFile, delimiter=',')
        for row in readcsv:
            if (row[0]) == str(Count):
                for Index,element in enumerate(row,0):
                    ElementName_HD = ElementName(Path_Config_Setting)
                    elementChecked = ElementName_HD.GetElementByName(str(Index),element,row)
                    GetContentDataFromCsv.append(elementChecked) 
    csvFile.close()
    return GetContentDataFromCsv
def checkLengthAngGetSumOfItemRafterFromCsv (path,Lr_Row):
        with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            sum = 0 
            for index,row in enumerate(readcsv):
                LengthRafter = row[8]
                if index == 0:
                    continue
                RafterName = row[5]
                Slope = row[13]
                Slope = UnitUtils.ConvertToInternalUnits(float(Slope), DisplayUnitType.DUT_DECIMAL_DEGREES)
                PlateThinessRaffter = float(row[9])
                if index==Lr_Row - 1 :
                    PlateThinessRaffter = float(row[9])/2
                if row[8] == "BAL":
                    if "4111" in RafterName: 
                        PlateThinessRaffter = PlateThinessRaffter/(math.cos(Slope))
                    sum = sum   + float (PlateThinessRaffter) * 2
                else: 
                    if ("4111" in RafterName) or (index==Lr_Row - 1) : 
                        PlateThinessRaffter = (PlateThinessRaffter * 2)/math.cos(Slope)
                        sum = sum + float(LengthRafter) + float(PlateThinessRaffter)
                    else:
                        sum = sum + float(LengthRafter) + float(PlateThinessRaffter) * 2
        csvFile.close()
        return sum