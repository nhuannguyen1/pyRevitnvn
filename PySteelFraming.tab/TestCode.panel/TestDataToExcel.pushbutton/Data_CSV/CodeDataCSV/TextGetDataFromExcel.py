import pandas as pd
from pandas import ExcelWriter,ExcelFile
import numpy as np
from openpyxl import load_workbook
from ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
from Csv_Excel import HandlingDataSTr,GetIndexOfNotChange,AligntText
from Path_Connect_Excel import Right_Genneral_All_path,Left_Genneral_All_path,DataExcel,Config_Setting_Path
#from Csv_Connect_Data import ReturnDataAllRowByIndexpath
book = load_workbook(DataExcel)
def CreateFileExcel():
    ArrPAth = [Left_Genneral_All_path,Right_Genneral_All_path]
    #IndexChange = ReturnDataAllRowByIndexpath(Config_Setting_Path,0)
    IndexChange =  [int(i) for i in  ReturnDataAllRowByIndexpath(Config_Setting_Path,0)]
    #IndexGeneral = ReturnDataAllRowByIndexpath(Config_Setting_Path,22)
    IndexGeneral = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,22)]
    #remove Column move 
    #Columnmove = ReturnDataAllRowByIndexpath(Config_Setting_Path,32)
    Columnmove = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,32)]

    LocationCellForMoveColumn = ReturnDataAllRowByIndexpath(Config_Setting_Path,34)
    s1 = set(IndexChange).difference(set(Columnmove))

    writer = ExcelWriter(DataExcel,engine='openpyxl')

    writer.book = book

    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    ArrMaxValue = IndexGeneral + Columnmove + IndexChange

    RangMax = range(max(ArrMaxValue) + 1)

    ArrRangMax = [* range(max(ArrMaxValue) + 1)]

    IndexChange1  = set(ArrRangMax).difference(set(IndexGeneral + Columnmove))
    IndexChangeRemoveColumn = set(IndexChange).difference(set(Columnmove))
    for path in ArrPAth:
        if path == Left_Genneral_All_path:
            df1 = pd.read_csv(path, delimiter=',',index_col = 0)
            dfCount = df1.shape
            df1.to_csv(path)
            df = pd.read_csv(path, delimiter=',',usecols = IndexGeneral,nrows= 1)
            #df.to_string(index=False)
            dfChange = pd.read_csv(path, delimiter=',',usecols = IndexChange1 )
            df.to_excel(writer,'General Member',index=False,header=False ,startcol=0,startrow=1)
            dfChange.to_excel(writer,'Left Member',index=False,header=False ,startcol=0,startrow=1, merge_cells=True)
            worksheet = writer.sheets['Left Member']
            #Wirte Column to csv
            for cell,index in zip(LocationCellForMoveColumn,Columnmove):
                cellstr = HandlingDataSTr(cell)
                df = pd.read_csv(path, delimiter=',',index_col = None ,usecols = [index],nrows= 1)
                worksheet.cell(row = cellstr[0], column = cellstr[1]).value = df.iat[0,0]
            IndexChangeTotal = list(IndexChange1)
            GetIndex = GetIndexOfNotChange(IndexChangeRemoveColumn,IndexChangeTotal)
            for index in GetIndex:
                worksheet.merge_cells(start_row=2, start_column=index + 1, end_row = (dfCount[0] + 1), end_column=index + 1)
            AligntText(worksheet)
        else:
            df1 = pd.read_csv(path, delimiter=',',index_col = 0)        
            df1.to_csv(path)
            dfChange = pd.read_csv(path, delimiter=',',index_col = None ,usecols = IndexChange1 )
            dfChange.to_excel(writer,'Right Member',index=False,header=False ,startcol=0,startrow=1,merge_cells=True)
            worksheet = writer.sheets['Right Member']
            for cell,index in zip(LocationCellForMoveColumn,Columnmove):
                cellstr = HandlingDataSTr(cell)
                df = pd.read_csv(path, delimiter=',',index_col = None ,usecols = [index],nrows= 1)
                worksheet.cell(row = cellstr[0], column = cellstr[1]).value = df.iat[0,0]
            IndexChangeTotal = list(IndexChange1)
            GetIndex = GetIndexOfNotChange(IndexChangeRemoveColumn,IndexChangeTotal)
            for index in GetIndex:
                worksheet.merge_cells(start_row=2, start_column=index + 1, end_row = (dfCount[0] + 1), end_column=index + 1)
            AligntText(worksheet)
    book.save('new_big_file.xlsx') 
CreateFileExcel()