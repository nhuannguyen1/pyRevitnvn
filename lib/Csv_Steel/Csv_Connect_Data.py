# coding: utf8
import csv
import math
#import ConvertAndCaculation
#from Autodesk.Revit.DB import UnitUtils,DisplayUnitType
class DataCSV:
    def  __init__(self, path):
        self.path = path
    def CountNumberOfRow (self):
        with open(self.path, 'r') as readFile:
            a = sum (1 for row in readFile)
        readFile.close
        return a
    def CountNumberOfColumn (self):
        file = self.path
        reader = csv.reader(open(file,'r'),delimiter=",")
        num_cols = len(next(reader))
        return num_cols
    def ArrFistForDefautValue(self):
        col = self.CountNumberOfColumn() 
        ArrFisrtData = []
        for i in range (0,col):
            ArrFisrtData.append(None)
            i +=1
        return ArrFisrtData
    def writefilecsvFromRowArr(self,Str_Row):
        with open(self.path, 'a') as csvFile:
            writer = csv.writer(csvFile,lineterminator='\n')
            writer.writerow(Str_Row)
        csvFile.close()
    def InputDataChangeToCSV(self,Count,row_input):
        with open(self.path, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[Count] = row_input
        with open(self.path, 'w') as writeFile:
            writer = csv.writer(writeFile,lineterminator='\n')
            writer.writerows(lines)
        writeFile.close()
        readFile.close()
    def DeleteRow(self,Count):
        ClearRow = []
        with open(self.path ,'rb') as inp:
            Count_Row = 0 
            for row in csv.reader(inp):
                    Count_Row += 1
                    if Count_Row > 2:
                        break
                    else:
                        ClearRow.append(row)
        ClearRow_N = [ClearRow[0],ClearRow[1]]
        with open(self.path, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile,lineterminator='\n')
            csv_writer.writerows(ClearRow_N)
        inp.close()
        csvfile.close()
    def writeRowTitle(self,Path_Conf):
        Str_Path_Conf =  self.ReturnDataAllRowByIndexpath(Path_Conf,9)
        Str_Path_Conf_Handling  =[]
        for ele in Str_Path_Conf:
            if "self." in ele:
                Str_Path_Conf_Handling.append(ele[5:])
            else:
                Str_Path_Conf_Handling.append(ele)
        with open(Path_Conf,'r') as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            lines = list(readcsv)
            lines[10] = Str_Path_Conf_Handling
        csvFile.close() 
        with open(Path_Conf, 'w') as writeFile:
                 writer = csv.writer(writeFile,lineterminator='\n')
                 writer.writerows(lines)
        writeFile.close()
        Str_Path_Conf =  self.ReturnDataAllRowByIndexpath(Path_Conf,10)
        with open(self.path,'r') as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            lines = list(readcsv)
            lines[0] = Str_Path_Conf
        csvFile.close() 
        with open(self.path, 'w') as writeFile:
                 writer = csv.writer(writeFile,lineterminator='\n')
                 writer.writerows(lines)
        writeFile.close()

    def SynChronizeValueToCSV (self,path):
        RowF0 = self.ReturnDataAllRowByIndexpath(path,0)
        del RowF0[0]
        countRow = self.CountNumberOfRow()
        with open(self.path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            lines = list(readcsv)
            ReturnFirstRow = self.ReturnDataAllRowByIndex(1)
            for indexCol in RowF0:
                for IndexRow in range(2,int(countRow)):
                    lines[int(IndexRow)][int(indexCol)] = ReturnFirstRow[int(indexCol)]
        csvFile.close() 
        with open(self.path, 'w') as writeFile:
                 writer = csv.writer(writeFile,lineterminator='\n')
                 writer.writerows(lines)
        writeFile.close()


    def SynChronizeValueToCSV1(self,path,Count):
        RowF0 = self.ReturnDataAllRowByIndexpath(path,0)
        del RowF0[0]
        countRow = self.CountNumberOfRow()
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',',lineterminator='\n')
            lines = list(readcsv)
            ReturnFirstRow = self.ReturnDataAllRowByIndex(Count)
            for indexCol in RowF0:
                for IndexRow in range(1,int(countRow)):
                    lines[int(IndexRow)][int(indexCol)] = ReturnFirstRow[int(indexCol)]
        csvFile.close() 
        with open(self.path, 'w') as writeFile:
                 writer = csv.writer(writeFile,lineterminator='\n')
                 writer.writerows(lines)
        writeFile.close()
    
    def SysWhenStart(self,Row,Count,path):
        RowF0 = self.ReturnDataAllRowByIndexpath(path,0)
        del RowF0[0]
        countRow = self.CountNumberOfRow()
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            lines = list(readcsv)
            #ReturnFirstRow = self.ReturnDataAllRowByIndex(Count)
            for indexCol in RowF0:
                for IndexRow in range(1,int(countRow)): 
                    lines[int(IndexRow)][int(indexCol)] = Row[int(indexCol)]
        csvFile.close() 
        with open(self.path, 'w') as writeFile:
                 writer = csv.writer(writeFile,lineterminator='\n')
                 writer.writerows(lines)
        writeFile.close()
    def ReturnDataAllRowByIndexpath (self,path,NumberRow):
        with open(path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        return RowNumber
    def ReturnFirstRow(self):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if row[0] =='1':
                    rowF  = row
                    break
        csvFile.close()
        return rowF
    def ReturnDataAllRowByIndex (self,NumberRow):
        with open(self.path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        return RowNumber
    def DataForLastRowIndex (self,CurrentCount,Str_Row):
        LastCount = self.CountNumberOfRow()
        if CurrentCount == LastCount:
            with open(self.path, 'a') as csvFile:
                writer = csv.writer(csvFile,lineterminator='\n')
                writer.writerow(Str_Row)
            csvFile.close()
class SaveDataToCSV:
    def  __init__(self, path):
        self.path = path
    def SaveDataH_tAndH_N(self,H_n,H_t):
        lines = [["H_n","H_t"],[H_n,H_t]]
        with open(self.path, 'w') as csvFile:
            writer = csv.writer(csvFile,lineterminator='\n')
            writer.writerows(lines)
        csvFile.close()
def ReturnArrContainSelectedAndText (path,NumberRowSelectedItem,NumberRowText, NumberTextModify,SelectedItem,Text):
        with open(path,"rU") as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            NumberRowSelectedItems = readcsv[NumberRowSelectedItem]
            NumberRowSelectedItems.pop(0)
            NumberRowTexts = readcsv[NumberRowText]
            NumberRowTexts.pop(0)
            arrTextModifyNumber = readcsv[NumberTextModify]
            for NumberRowSelectedItem in NumberRowSelectedItems:
                arrTextModifyNumber[int(NumberRowSelectedItem)] = arrTextModifyNumber[int(NumberRowSelectedItem)] + "." + SelectedItem
            for NumberRowText in NumberRowTexts:
                arrTextModifyNumber[int(NumberRowText)] = arrTextModifyNumber[int(NumberRowText)] + "." + Text
        csvFile.close()
        return arrTextModifyNumber
def GetDataToPrimaryFile (path1,path2,path_Conf,Count):
    DataCSVP2 = DataCSV(path2)
    DataCSVP1 = DataCSV(path1)
    DataCSVPConf = DataCSV(path_Conf)
    RowCount = DataCSVP2.CountNumberOfRow()
    RowF0 = DataCSVPConf.ReturnDataAllRowByIndexpath(path_Conf,11)
    del RowF0[0]
    with open(path1, 'rU') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            row_input = lines[Count]
            Row_Input1 = [row_input[int(vt)] for vt in RowF0]
    with open(path2, 'rU') as writeFile:
        reader = csv.reader(writeFile)
        lines = list(reader)
        for count,index in enumerate(RowF0,0) :
            for i in range(1,RowCount):
                lines[int(i)][int(index)] = Row_Input1[count]
    with open(path2, 'w') as writeFile1:
                writer = csv.writer(writeFile1,lineterminator='\n')
                writer.writerows(lines)
    writeFile.close()
    readFile.close()
    writeFile1.close()
