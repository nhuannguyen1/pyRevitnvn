import os
from Csv_Connect_Data import DataCSV,SaveDataToCSV
from DirectoryPath import Path_Config_Setting,dir_path,ReturnPath
ArrPath = ReturnPath()
Right_Member_All = ArrPath[8]
Left_DataSaveToCaculation = ArrPath[1]
from ConvertAndCaculation import FindV34,GetSlope,FindSlopeFromPHandEV,GetSlopetEhAndPh
PathTemplate = DataCSV (Path_Config_Setting)
def GetFixLevel (count):
    GetFixLevelrt = PathTemplate.ReturnDataAllRowByIndex(count)
    return GetFixLevelrt
def GetParameterName (path):
    BaseName = os.path.basename(path)
    ArrSlope = PathTemplate.ReturnDataAllRowByIndex(3)
    ArrPathName = PathTemplate.ReturnDataAllRowByIndex(2)
    for index,ele in enumerate (ArrPathName):
        if (BaseName == ele) and index == 7:
            SlopeName = ArrSlope[0]
            break
        else:
            if (BaseName == ele) and index == 8:
                SlopeName = ArrSlope[1]
                break
    return SlopeName
def GetSelectLevel(path, Select_Level,Clear_Height,Peak_Height,Eave_Height,Slope,Offset_Top_Level,Top_Level_Col,Base_Leveled_Point,ColumnCreate,X_Left,X_Right,Length_From_Gird):
    GetFixLevellr =GetFixLevel(5)
    if path != Right_Member_All:
        if (Select_Level == GetFixLevellr[0]):
            Offset_Top_Level1 = Offset_Top_Level
            Slope = Slope
        elif (Select_Level == GetFixLevellr[1]):
            ArrSL = FindSlopeFromPHandEV(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right,Clear_Height,Peak_Height,Length_From_Gird)
            Slope = ArrSL[0]
            Offset_Top_Level1 = float (0)
        elif (Select_Level == GetFixLevellr[2]):
            Offset_Top_Level1 = FindV34(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right)
            Slope = Slope
        elif (Select_Level == GetFixLevellr[3]):
            Slope = GetSlope(Eave_Height,Peak_Height,Length_From_Gird)
            Offset_Top_Level1 = FindV34(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right)
        else:
            print ("Other Case ")
        return [Slope,Offset_Top_Level1]
    else:
        Data = DataCSV(Left_DataSaveToCaculation)
        Strarr = Data.ReturnDataAllRowByIndexpath(Left_DataSaveToCaculation,1)
        if (Select_Level == GetFixLevellr[1]):
            ElevationCH = Clear_Height.Elevation
            Peak_Height = float(Strarr[1]) 
            ArrSL = FindSlopeFromPHandEV(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right,ElevationCH,Peak_Height,Length_From_Gird)
            V_CH = ArrSL[1]
            #ElevationEH = Eave_Height.Elevation
            ElevationEH  = float(ElevationCH) + float (V_CH)
            #Peak_Height = float(Strarr[1]) + float(ElevationCH)
            #Slope = ArrSL[0]
            Slope = GetSlopetEhAndPh(ElevationEH,Peak_Height,Length_From_Gird)
            Offset_Top_Level1 = float (0)
            return [Slope,Offset_Top_Level1]
        elif (Select_Level == GetFixLevellr[3]):
            #Peak_Height = float(Strarr[1]) + float(ElevationEH)
            Peak_Height = float(Strarr[1])
            ElevationEH = Eave_Height.Elevation
            Slope = GetSlopetEhAndPh(ElevationEH,Peak_Height,Length_From_Gird)
            Offset_Top_Level1 = FindV34(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right)
            return [Slope,Offset_Top_Level1]
        else:
            print (" ReCheck select member level")