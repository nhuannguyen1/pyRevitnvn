import os
from Csv_Connect_Data import DataCSV,SaveDataToCSV
from DirectoryPath import Path_Config_Setting,dir_path
PathTemplate = DataCSV (Path_Config_Setting)
def GetParameterName (path):
    BaseName = os.path.basename(path)
    ArrSlope = PathTemplate.ReturnDataAllRowByIndex(3)
    ArrPathName = PathTemplate.ReturnDataAllRowByIndex(2)
    for index,ele in enumerate (ArrPathName):
        if BaseName == ele:
            SlopeName = ArrSlope[index]
    return SlopeName