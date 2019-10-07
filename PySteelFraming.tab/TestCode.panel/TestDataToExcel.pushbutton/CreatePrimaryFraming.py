import csv
from Csv_Connect_Data import DataCSV
from DirectoryPath import Path_Config_Setting,ReturnPath
#Path_Config_Setting = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Config_Setting.csv"
from GlobalParameter import DataFromCSV
import CreateMiddlemenElement
DataCSV_C = DataCSV(Path_Config_Setting)
#ArrPath = DataCSV_C.ReturnDataAllRowByIndex(2)
ArrPath = ReturnPath()
def PrimaryFraming():
    for index,path in enumerate(ArrPath):
        if index in [int(0),int(1)]:
            DataCSV_C = DataCSV(path)
            DataCSV_C.SynChronizeValueToCSV(Path_Config_Setting)
            DataFromCsv_New  = DataCSV(path)
            ArrDataExcell = DataFromCsv_New.ArrFistForDefautValue()
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            DataFromdem.SetPath(path)
            arr = DataFromdem.GetContentDataFromExcel(path)
            DataFromdem = DataFromCSV(*arr)
            if index == 0 :
                DataFromdem.CreateElement()
            else:
                ReturnARR = DataFromdem.CreateElement()
                CreateMiddlemenElement.CreateElementByMirror(ReturnARR[0],ReturnARR[1],ReturnARR[2])