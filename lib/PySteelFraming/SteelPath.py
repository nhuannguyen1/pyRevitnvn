import csv
import os
class PathSteel:
    def  __init__(self, path = None,dir_path = None,FolderName = None):
            self.path = path
            self.dir_path = dir_path
            self.FolderName = FolderName
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
    def ReturnPath (self):
        #dir_path is directory to folder store conf seting csv 
        ArrPath = self.ReturnDataAllRowByIndexpathIncludeIndex0(2)
        Genneral_Parameter =self.ReturnPath_Conf(ArrPath[0])
        Left_DataSaveToCaculation = self.ReturnPath_Conf(ArrPath[1])
        Left_Member_Change = self.ReturnPath_Conf(ArrPath[2])
        Left_Member_Change_U = self.ReturnPath_Conf(ArrPath[3])
        Right_DataSaveToCaculation = self.ReturnPath_Conf(ArrPath[4])
        Right_Member_Change = self.ReturnPath_Conf(ArrPath[5])
        Right_Member_Change_U = self.ReturnPath_Conf(ArrPath[6])
        Left_Genneral = self.ReturnPath_Conf(ArrPath[7])
        Right_Genneral = self.ReturnPath_Conf(ArrPath[8])
        return [Genneral_Parameter,Left_DataSaveToCaculation,Left_Member_Change,\
        Left_Member_Change_U,Right_DataSaveToCaculation,Right_Member_Change,\
            Right_Member_Change_U,Left_Genneral,Right_Genneral]
    def ReturnPath_Conf(self,Name_File):
        dir_path = self.dir_path + "\\" + self.FolderName
        full_path = os.path.join(dir_path,Name_File)
        return full_path
    def ReturnDataAllRowByIndexpathIncludeIndex0 (self,NumberRow):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        return RowNumber
    def SetPath(self,NewValuePath):
        self.path = NewValuePath