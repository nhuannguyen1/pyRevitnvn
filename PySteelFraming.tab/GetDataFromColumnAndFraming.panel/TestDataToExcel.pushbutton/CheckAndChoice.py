import os
from Csv_Steel.Csv_Connect_Data import DataCSV
from ConvertAndCaculation import CaculateForFraming
from PySteelFraming.SteelPath import PathSteel
class CheckChoice:
    def  __init__(self, path = None, Path_Config_Setting = None, Select_Level = None,Clear_Height = None,Peak_Height = None ,Eave_Height = None ,Slope = None,\
        Offset_Top_Level  = None,Top_Level_Col  = None,ColumnCreate = None ,X_Left = None,X_Right = None ,Length_From_Gird = None,\
            GetElementType = None ,ElevationCH = None, LengthPurlin = None):
            self.path = path
            self.Path_Config_Setting = Path_Config_Setting
            self.Select_Level = Select_Level
            self.Clear_Height = Clear_Height
            self.Peak_Height = Peak_Height
            self.Eave_Height = Eave_Height
            self.Slope = Slope
            self.Offset_Top_Level = Offset_Top_Level
            self.Top_Level_Col = Top_Level_Col
            self.ColumnCreate = ColumnCreate
            self.X_Left = X_Left
            self.X_Right = X_Right
            self.Length_From_Gird = Length_From_Gird
            self.GetElementType = GetElementType
            self.ElevationCH = ElevationCH
            self.LengthPurlin = LengthPurlin
            self.PathSteel_Hd = PathSteel(path = self.Path_Config_Setting,Is_Directory_Path_To_Config = True)
            self.ArrPath = self.PathSteel_Hd.ReturnPath()
            self.Right_Member_All = self.ArrPath[8]
            self.Left_DataSaveToCaculation = self.ArrPath[1]
    def GetSelectLevel(self):
        # get arr select level choice 
        GetFixLevellr = self.PathSteel_Hd.ReturnDataAllRowByIndexpathIncludeIndex0(5)
        if self.path  != self.Right_Member_All :
            if (self.Select_Level == GetFixLevellr[0]):
                Offset_Top_Level1 = float(0)
                Slope = self.Slope 
            elif (self.Select_Level == GetFixLevellr[1]):
                Clear_Height = self.Clear_Height.Elevation
                Peak_Height = self.Peak_Height.Elevation
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,Slope = self.Slope,\
                Offset_Top_Level= self.Offset_Top_Level,X_Left_X=self.X_Left,X_Right_X=self.X_Right,CH= Clear_Height,\
                PH=Peak_Height,Length=self.Length_From_Gird,LengthPurlin= self.LengthPurlin,Path_Config_Setting = self.Path_Config_Setting)
                ArrSL = CaculateForFramingHd.FindSlopeFromPHandEV()
                Slope = ArrSL[0]
                Offset_Top_Level1 = float (0)
            elif (self.Select_Level == GetFixLevellr[2]):
                #Clear_Height = self.Clear_Height.Elevation
                #Peak_Height = self.Peak_Height.Elevation
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,Slope = self.Slope,\
                Offset_Top_Level= self.Offset_Top_Level,X_Left_X=self.X_Left,X_Right_X=self.X_Right,\
                Length=self.Length_From_Gird,LengthPurlin= self.LengthPurlin,Path_Config_Setting = self.Path_Config_Setting)
                Offset_Top_Level1 = CaculateForFramingHd.FindV34() 
                Slope = self.Slope
            elif (self.Select_Level == GetFixLevellr[3]):
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,EH = self.Eave_Height,PH= self.Peak_Height, Length=self.Length_From_Gird)
                Slope = CaculateForFramingHd.GetSlope()
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,EH = self.Eave_Height,PH= self.Peak_Height,\
                     Length=self.Length_From_Gird,Slope=Slope,X_Left_X=self.X_Left,X_Right_X=self.X_Right,LengthPurlin=self.LengthPurlin,\
                         Offset_Top_Level=self.Offset_Top_Level)
                Offset_Top_Level1 = CaculateForFramingHd.FindV34()
            else:
                print ("Other Case ")
            return [Slope,Offset_Top_Level1]
        else:
            Data = DataCSV(self.Left_DataSaveToCaculation)
            Strarr = Data.ReturnDataAllRowByIndexpath(self.Left_DataSaveToCaculation,1)
            if (self.Select_Level == GetFixLevellr[1]):
                ElevationCH = self.Clear_Height.Elevation
                Peak_Height = float(Strarr[1])
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,Slope = self.Slope,\
                Offset_Top_Level= self.Offset_Top_Level,X_Left_X=self.X_Left,X_Right_X=self.X_Right,CH= ElevationCH,\
                PH=Peak_Height,Length=self.Length_From_Gird,LengthPurlin= self.LengthPurlin,Path_Config_Setting = self.Path_Config_Setting)
                ArrSL = CaculateForFramingHd.FindSlopeFromPHandEV()
                V_CH = ArrSL[1]
                ElevationEH  = float(ElevationCH) + float (V_CH)
                CaculateForFramingHd = CaculateForFraming (EH=ElevationEH,PH= Peak_Height,Length=self.Length_From_Gird)
                Slope = CaculateForFramingHd.GetSlopetEhAndPh()
                Offset_Top_Level1 = float(0)
            elif (self.Select_Level == GetFixLevellr[2]):
                ElevationPH = float(Strarr[1]) 
                ElevationEH = self.Eave_Height.Elevation
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,Slope = self.Slope,\
                Offset_Top_Level= self.Offset_Top_Level,X_Left_X=self.X_Left,X_Right_X=self.X_Right,\
                Length=self.Length_From_Gird,LengthPurlin= self.LengthPurlin,ElevationEH=ElevationEH,ElevationPH=ElevationPH)
                Offset_Top_Level1 = CaculateForFramingHd.FindOffsetLevel() 
                Slope = self.Slope
            elif (self.Select_Level == GetFixLevellr[3]):
                LengthPurlin = float(0)
                Peak_Height = float(Strarr[1])  + float(self.LengthPurlin)

                #Peak_Height = float(Strarr[1]) + LengthPurlin
                ElevationEH = self.Eave_Height.Elevation
                CaculateForFramingHd = CaculateForFraming (EH=ElevationEH,PH= Peak_Height,Length=self.Length_From_Gird)
                Slope = CaculateForFramingHd.GetSlopetEhAndPh()
                CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,EH = self.Eave_Height,PH= self.Peak_Height,\
                    Length=self.Length_From_Gird,Slope=Slope,X_Left_X=self.X_Left,X_Right_X=self.X_Right,LengthPurlin=self.LengthPurlin,\
                        Offset_Top_Level=self.Offset_Top_Level)
                Offset_Top_Level1 = CaculateForFramingHd.FindV34() 
            else:
                print (" ReCheck select member level")
            return [Slope,Offset_Top_Level1]
    def CheckAndReturnX_RightAndX_Left (self):
        GetFixLevellr = self.PathSteel_Hd.ReturnDataAllRowByIndexpathIncludeIndex0(4)
        Data = DataCSV(Left_DataSaveToCaculation)
        Strarr = Data.ReturnDataAllRowByIndexpath(Left_DataSaveToCaculation,1)
        ElevationPH = float(Strarr[1]) 
        if (self.path == Right_Member_All and (self.Select_Level == GetFixLevellr[2])):
            ElevationEH = self.ElevationEH.Elevation
            CaculateForFramingHd = CaculateForFraming (ElementInstance=self.ColumnCreate,Slope = self.Slope,\
            Offset_Top_Level= self.Offset_Top_Level,X_Left_X=self.X_Left,X_Right_X=self.X_Right,CH= Clear_Height,\
            PH=Peak_Height,Length=self.Length_From_Gird,LengthPurlin= self.LengthPurlin,ElevationPH=ElevationPH,ElevationEH=ElevationEH)
            FindX_RightAndX_Left1 = CaculateForFramingHd.FindX_RightAndX_Left (self.Slope,self.X_Left_X,self.X_Right_X,self.Length,ElevationEH,ElevationPH)
            X_Left_X = FindX_RightAndX_Left1[0]
            X_Right_X = FindX_RightAndX_Left1[1]
        return [X_Left_X,X_Right_X]