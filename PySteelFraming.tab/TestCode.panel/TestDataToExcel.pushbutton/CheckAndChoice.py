import os
from Csv_Connect_Data import DataCSV,SaveDataToCSV
from DirectoryPath import Path_Config_Setting,dir_path
from ConvertAndCaculation import FindV34,GetSlope,FindV34_1
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
    if (Select_Level == GetFixLevellr[0]):
        Offset_Top_Level1 = Offset_Top_Level
        Slope = Slope
    elif (Select_Level == GetFixLevellr[1]):
        #Slope = FindV34_1(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right,Clear_Height,Peak_Height,Length_From_Gird)
        print (Slope)
    elif (Select_Level == GetFixLevellr[2]):
        Offset_Top_Level1 = FindV34(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right)
        Slope = Slope
    elif (Select_Level == GetFixLevellr[3]):
        Slope = GetSlope(Eave_Height,Peak_Height,Length_From_Gird)
        Offset_Top_Level1 = FindV34(ColumnCreate,Slope,Offset_Top_Level,X_Left,X_Right)
    else:
        print ("Other Case ")
    return [Slope,Offset_Top_Level1]