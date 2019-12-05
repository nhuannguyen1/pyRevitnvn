import os
from PySteelFraming.SteelPath import PathSteel
class CheckChoice:
    def  __init__(self, path = None):
        self.path = path
        self.PathSteelHD = PathSteel(self.path)
    def Get_Level_Selected (self,count):
        GetFixLevelrt = self.PathSteelHD.ReturnDataAllRowByIndexpathIncludeIndex0(count)
        return GetFixLevelrt
    def GetParameterName (self):
        BaseName = os.path.basename(path)
        ArrSlope = self.PathSteelHD.ReturnDataAllRowByIndexpathIncludeIndex0(3)
        ArrPathName = self.PathSteelHD.ReturnDataAllRowByIndexpathIncludeIndex0(2)
        for index,ele in enumerate (ArrPathName):
            if (BaseName == ele) and index == 7:
                SlopeName = ArrSlope[0]
                break
            else:
                if (BaseName == ele) and index == 8:
                    SlopeName = ArrSlope[1]
                    break
        return SlopeName
