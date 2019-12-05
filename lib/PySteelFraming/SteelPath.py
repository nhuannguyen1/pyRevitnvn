from pathlib import Path
class PathSteel:
    def  __init__(self, path = None,dir_path = None,FolderName = None,\
        Is_Directory_Path_To_Config = False,Path_Conf = None, FileName = None):
            self.path = path
            self.dir_path = dir_path
            self.FolderName = FolderName
            self.Path_Conf = Path_Conf
            self.Is_Directory_Path_To_Config = Is_Directory_Path_To_Config
            self.FileName = FileName
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
        if self.dir_path != None:
            pass
        else:
            self.Set_DirPath(os.path.dirname(self.path))
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
    # return conf path 
    def ReturnPath_Conf(self,Name_File):
        if self.Is_Directory_Path_To_Config == False:
            dir_path = self.dir_path + "\\" + self.FolderName
            full_path = os.path.join(dir_path,Name_File)
        else:
            full_path = os.path.join(self.dir_path,Name_File)
        return full_path
    # return All row by index path include index 0 
    def ReturnDataAllRowByIndexpathIncludeIndex0 (self,NumberRow):
        with open(self.path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        return RowNumber
    def SetPath(self,NewValuePath):
        self.path = NewValuePath
    def ReturnDataAllRowByIndexpathTest (self,NumberRow):
        with open(self.path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        del RowNumber[0]
        return RowNumber
    # return all value from index path 
    def Get_Level_Selected (self,count):
        GetFixLevelrt = self.ReturnDataAllRowByIndexpathIncludeIndex0(count)
        return GetFixLevelrt
    # Get Slope parameter 
    def GetParameterName (self):
        BaseName = os.path.basename(self.path)
        ArrSlope = self.ReturnDataAllRowByIndexpathIncludeIndex0_paTH(3,self.Path_Conf)
        ArrPathName = self.ReturnDataAllRowByIndexpathIncludeIndex0_paTH(2,self.Path_Conf)
        for index,ele in enumerate (ArrPathName):
            if (BaseName == ele) and index == 7:
                SlopeName = ArrSlope[0]
                break
            else:
                if (BaseName == ele) and index == 8:
                    SlopeName = ArrSlope[1]
                    break
        return SlopeName
    def Set_DirPath(self,Value_DirPath):
        self.dir_path = Value_DirPath
    def ReturnDataAllRowByIndexpathIncludeIndex0_paTH (self,NumberRow,path):
        with open(path,"rU") as csvFile:
            readcsv = csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
            csvFile.close()
        return RowNumber
