# coding: utf8
import csv
import GetElementByName
import os.path
import math
import ConvertAndCaculation
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
            writer = csv.writer(csvFile)
            writer.writerow(Str_Row)
        csvFile.close()
    def GetContentDataByName(self,Count):
        GetContentDataFromCsv = []
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            for row in readcsv:
                if (row[0]) == str(Count):
                    for Index,element in enumerate(row,0):
                        elementChecked = GetElementByName.GetElementByName(str(Index),element,row)
                        GetContentDataFromCsv.append(elementChecked) 
        csvFile.close()
        return GetContentDataFromCsv
    def InputDataChangeToCSV(self,Count,row_input):
        with open(self.path, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[Count] = row_input
        with open(self.path, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        writeFile.close()
        readFile.close()
    def checkLengthAngGetSumOfItemRafterFromCsv (self,Lr_Row):
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            sum = 0 
            for index,row in enumerate(readcsv):
                LengthRafter = row[8]
                if row[8] == "Length":
                    continue
                RafterName = row[5]
                Slope = row[13]
                Slope = ConvertAndCaculation.ConvertToInternalUnitDegree(Slope)
                PlateThinessRaffter = float(row[9])
                if index==Lr_Row - 1 :
                    PlateThinessRaffter = float(row[9])/2
                if row[8] == "BAL":
                    if "4111" in RafterName: 
                        PlateThinessRaffter = PlateThinessRaffter/(math.cos(Slope))
                    sum = sum   + float (PlateThinessRaffter) * 2
                else:
                    if ("4111" in RafterName) or (index==Lr_Row - 1) : 
                        PlateThinessRaffter = (PlateThinessRaffter * 2)/math.cos(Slope)
                        sum = sum + float(LengthRafter) + float(PlateThinessRaffter)
                    else:
                        sum = sum + float(LengthRafter) + float(PlateThinessRaffter) * 2
        csvFile.close()
        return sum
   
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
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(ClearRow_N)
        inp.close()
        csvfile.close()
    def writeRowTitle(self): 
        with open(self.path,'w') as f:
            f.write('STT,Family Column,Family Column Type,Base Level,Top Level,Family Rafter,\
                Family Type Rafter,Level Rafter,Length,Plate,Path,Gird_Ver,Gird_Hor,Slope,\
                    Gird_Ver,Gird_Hor,Length From Gird,Plate Column,\
                        Move Left,Move Right,Move Up,Move Bottom,Top Offset Level\n') 
        f.close()
    def SynChronizeValueToCSV (self,path):
        RowF0 = self.ReturnDataAllRowByIndexpath(path,0)
        del RowF0[0]
        countRow = self.CountNumberOfRow()
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            lines = list(readcsv)
            ReturnFirstRow = self.ReturnDataAllRowByIndex(1)
            for indexCol in RowF0:
                for IndexRow in range(2,int(countRow)): 
                    lines[int(IndexRow)][int(indexCol)] = ReturnFirstRow[int(indexCol)]
        csvFile.close() 
        with open(self.path, 'w') as writeFile:
                 writer = csv.writer(writeFile)
                 writer.writerows(lines)
        writeFile.close()
    def ReturnDataAllRowByIndexpath (self,path,NumberRow):
        with open(path) as csvFile:
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
        with open(self.path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        return RowNumber
class SaveDataToCSV:
    def  __init__(self, path):
        self.path = path
    def SaveDataH_tAndH_N(self,H_n,H_t):
        lines = [["H_n","H_t"],[H_n,H_t]]
        with open(self.path, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(lines)
        csvFile.close()