import csv
import os
class PathSteel:
    def  __init__(self, path ):
            self.path = path
    #Return element Arr follow number of row 
    def ReturnDataAllRowByIndexpath (self,NumberRow):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=';')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        RowNumber.pop(0)
        return RowNumber
    #Return element Arr follow number all row    
    def ReturnDataAllRowByIndexpathAll(self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=';')
            readcsv = list(readcsv)
        csvFile.close()
        return readcsv
    def ReturnPath (self,dir_path):
        #dir_path is directory to folder store conf seting csv 
        ArrPath = ReturnDataAllRowByIndex_path(self.path ,2)
        Genneral_Parameter =os.path.join(dir_path,ArrPath[0])
        Left_DataSaveToCaculation = os.path.join(dir_path,ArrPath[1])
        Left_Member_Change = os.path.join(dir_path,ArrPath[2])
        Left_Member_Change_U = os.path.join(dir_path,ArrPath[3])
        Right_DataSaveToCaculation = os.path.join(dir_path,ArrPath[4])
        Right_Member_Change = os.path.join(dir_path,ArrPath[5])
        Right_Member_Change_U = os.path.join(dir_path,ArrPath[6])
        Left_Genneral = os.path.join(dir_path,ArrPath[7])
        Right_Genneral = os.path.join(dir_path,ArrPath[8])
        return [Genneral_Parameter,Left_DataSaveToCaculation,Left_Member_Change,\
        Left_Member_Change_U,Right_DataSaveToCaculation,Right_Member_Change,\
            Right_Member_Change_U,Left_Genneral,Right_Genneral]
"""
import os
import csv
#from Csv_Connect_Data import DataCSV
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path + "\\Data_CSV"
filename = "Config_Setting.csv"
full_path = os.path.join(dir_path,filename)
Path_Config_Setting = full_path
def ReturnDataAllRowByIndex_path(path,NumberRow):
    with open(path) as csvFile:
        readcsv =csv.reader(csvFile, delimiter=',')
        readcsv = list(readcsv)
        RowNumber = readcsv[NumberRow]
    csvFile.close()
    return RowNumber
#PathTemplate = DataCSV (Path_Config_Setting)
ArrPath = ReturnDataAllRowByIndex_path(Path_Config_Setting,2)
Genneral_Parameter =os.path.join(dir_path,ArrPath[0])
Left_DataSaveToCaculation = os.path.join(dir_path,ArrPath[1])
Left_Member_Change = os.path.join(dir_path,ArrPath[2])
Left_Member_Change_U = os.path.join(dir_path,ArrPath[3])
Right_DataSaveToCaculation = os.path.join(dir_path,ArrPath[4])
Right_Member_Change = os.path.join(dir_path,ArrPath[5])
Right_Member_Change_U = os.path.join(dir_path,ArrPath[6])
Left_Genneral = os.path.join(dir_path,ArrPath[7])
Right_Genneral = os.path.join(dir_path,ArrPath[8])
def ReturnPath ():
    return [Genneral_Parameter,Left_DataSaveToCaculation,Left_Member_Change,\
        Left_Member_Change_U,Right_DataSaveToCaculation,Right_Member_Change,\
            Right_Member_Change_U,Left_Genneral,Right_Genneral]
"""