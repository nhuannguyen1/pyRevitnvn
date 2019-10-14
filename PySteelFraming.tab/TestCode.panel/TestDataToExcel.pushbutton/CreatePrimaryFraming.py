import csv
from Csv_Connect_Data import DataCSV
import DirectoryPath
from DirectoryPath import Path_Config_Setting
from GlobalParameter import DataFromCSV
import CreateMiddlemenElement
DataCSV_C = DataCSV(Path_Config_Setting)
ArrPathIn = DirectoryPath.ReturnPath()
def PrimaryFraming():
    for index,path in enumerate(ArrPathIn):
        if index in [int(7),int(8)]:
            DataCSV_C = DataCSV(path)
            DataCSV_C.SynChronizeValueToCSV(Path_Config_Setting)
            DataFromCsv_New  = DataCSV(path)
            ArrDataExcell = DataFromCsv_New.ArrFistForDefautValue()
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            DataFromdem.SetPath(path)
            arr = DataFromdem.GetContentDataFromExcel(path,1)
            DataFromdem = DataFromCSV(*arr)
            if index == 7 :
                DataFromdem.CreateElement()
            else:
                ReturnARR = DataFromdem.CreateElement()
                CreateMiddlemenElement.CreateElementByMirror(ReturnARR[0],ReturnARR[1],ReturnARR[2])