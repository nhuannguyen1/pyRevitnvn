import pandas as pd
import Pynvn
from pandas import ExcelWriter,ExcelFile
import numpy as np
from openpyxl import load_workbook
from Pynvn.ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
from Pynvn.Csv_Excel import AligntText,ValueGeneral,Columnmove,LocationCellForMoveColumn,\
    GenneralColumnNotChange,GeneralConcernRaffter,Genneral_Select,LocationOfRowLeft,LocationOfRowRight,\
        ExcelCellForMoveColumnRight,LocationOfPurlin,WriteMoveColumn,Write_Path_ToExcel,startrow
from Path_Connect_Excel import Right_Genneral_All_path,Left_Genneral_All_path,DataExcel
import openpyxl
import os
path = os.path.abspath(openpyxl.__file__)
#from Csv_Connect_Data import ReturnDataAllRowByIndexpath
book = load_workbook(DataExcel)
def CreateFileExcel():
    writer = ExcelWriter(DataExcel,engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    #ArrMaxValue = IndexGeneral + Columnmove + IndexChange
    for path in [Left_Genneral_All_path,Right_Genneral_All_path]:
            df1 = pd.read_csv(path, delimiter=',',index_col = 0)
            dfCount = df1.shape
            df1.to_csv(path)
            #write Left to Excel 
            dfValueGeneral = pd.read_csv(path, delimiter=',',usecols = ValueGeneral,nrows= 1)
            dfValueGeneral.to_excel(writer,'General Member',index=False,header=True ,startcol=0,startrow= int(startrow[0]))
            worksheet = writer.sheets['General Member']
            if path == Left_Genneral_All_path:
                usecolsArr = LocationOfRowLeft
                LocationMoveColumn = LocationCellForMoveColumn
                #write path to excel 
                Write_Path_ToExcel(worksheet,path)
            else:
                usecolsArr = LocationOfRowRight
                LocationMoveColumn = ExcelCellForMoveColumnRight
                #write path to excel 
                Write_Path_ToExcel(worksheet,path)
            #Write genneral to excel
            DfChangegenneral = pd.read_csv(path, delimiter=',',usecols = GenneralColumnNotChange,nrows= 1 )
            DfChangegenneral.to_excel(writer,'General Member',index=False,header=True ,startcol=0,startrow= int(usecolsArr[1]) )
            #write Genneral Concern Raffter
            DfChangegenneral = pd.read_csv(path, delimiter=',',usecols = GeneralConcernRaffter )
            DfChangegenneral.to_excel(writer,'General Member',index=False,header=True ,startcol=0,startrow=int(usecolsArr[2]))
            #write genneral selected 
            DfChangegenneral = pd.read_csv(path, delimiter=',',usecols = Genneral_Select,nrows= 1)
            DfChangegenneral.to_excel(writer,'General Member',index=False,header=True ,startcol=0,startrow= int(usecolsArr[0]))
            #write purlin roof 
            DfChangegenneral = pd.read_csv(path, delimiter=',',usecols = LocationOfPurlin,nrows= 1)
            DfChangegenneral.to_excel(writer,'General Member',index=False,header=True ,startcol=0,startrow= int(usecolsArr[3]))
            worksheet = writer.sheets['General Member']
            #Wirte move Column to csv
            WriteMoveColumn(pd,worksheet,path,LocationMoveColumn,Columnmove)
            # align text for worksheet 
            AligntText(worksheet)
    book.save('new_big_file.xlsx') 