import csv
from Csv_Steel.Csv_Connect_Data import DataCSV
from GlobalParameter import DataFromCSV
from PySteelFraming.SteelPath import PathSteel
import CreateMiddlemenElement
class CreateFraming:
    def  __init__(self, path):
        self.path = path
        self.DataCSV_C = DataCSV(self.path)
        self.PathSteelHD = PathSteel(path = self.path,Is_Directory_Path_To_Config = True)
        self.ArrPathIn = self.PathSteelHD.ReturnPath()
    def PrimaryFraming(self):
        for index,path in enumerate(self.ArrPathIn):
            if index in [int(7),int(8)]:
                self.DataCSV_C.SynChronizeValueToCSV(self.path)
                ArrDataExcell = self.DataCSV_C.ArrFistForDefautValue()
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