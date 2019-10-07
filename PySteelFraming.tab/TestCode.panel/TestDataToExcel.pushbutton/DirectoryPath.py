import os
from Csv_Connect_Data import DataCSV
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "Config_Setting.csv"
full_path = os.path.join(dir_path,filename)
Path_Config_Setting = full_path
PathTemplate = DataCSV (Path_Config_Setting)
ArrPath = PathTemplate.ReturnDataAllRowByIndex(2)
def ReturnPath ():
    DataToolTemplate_Right =os.path.join(dir_path,ArrPath[0])
    DataToolTemplate_Left = os.path.join(dir_path,ArrPath[1])
    DataSaveToCaculation = os.path.join(dir_path,ArrPath[2])
    return [DataToolTemplate_Right,DataToolTemplate_Left,DataSaveToCaculation]