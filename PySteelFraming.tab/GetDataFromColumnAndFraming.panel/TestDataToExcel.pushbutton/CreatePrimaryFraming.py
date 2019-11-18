import csv
from Csv_Steel.Csv_Connect_Data import DataCSV
from GlobalParameter import DataFromCSV
from PySteelFraming.SteelPath import PathSteel
import CreateMiddlemenElement
class CreateFraming:
    def  __init__(self, path = None, PathRight = None,Left_DataSaveToCaculation = None):
        self.path = path
        self.PathRight = PathRight
        self.DataCSV_C = DataCSV(self.path)
        self.PathSteelHD = PathSteel(path = self.path,Is_Directory_Path_To_Config = True)
        self.ArrPathIn = self.PathSteelHD.ReturnPath()
        self.Left_DataSaveToCaculation = Left_DataSaveToCaculation
    def PrimaryFraming(self):
        for index,path in enumerate(self.ArrPathIn):
            if index in [int(7),int(8)]:
                DataCSV_C = DataCSV(path)
                DataCSV_C.SynChronizeValueToCSV(self.path)
                ArrDataExcell = self.DataCSV_C.ArrFistForDefautValue()
                DataFromdem = DataFromCSV(*ArrDataExcell,Path_Config_Setting=self.path,Right_Member_All=self.PathRight)
                DataFromdem.Set_Count(1)
                DataFromdem.SetPath(path)
                arr = DataFromdem.GetContentDataFromExcel(path,1)
                print ("self.Left_DataSaveToCaculation ",self.Left_DataSaveToCaculation )
                DataFromdem = DataFromCSV(*arr,Path_Config_Setting=self.path,Right_Member_All=self.PathRight,Left_DataSaveToCaculation=self.Left_DataSaveToCaculation )
                if index == 7 :
                    DataFromdem.CreateElement()
                else:
                    ReturnARR = DataFromdem.CreateElement()
                    CreateMiddlemenElement.CreateElementByMirror(ReturnARR[0],ReturnARR[1],ReturnARR[2])