import pandas as pd
from openpyxl import load_workbook
from Path_Connect_Excel import Right_Genneral_All_path,Left_Genneral_All_path,DataExcel,Config_Setting_Path
from Csv_Excel import HandlingDataSTr,GetIndexOfNotChange,AligntText,ValueGeneral,Columnmove,LocationCellForMoveColumn,ValueChangeLeft_Right,IndexChangeRemoveColumn
from CreateDicBetweenCsvAndFile import DicAndCsvExell
#from Csv_Connect_Data import ReturnDataAllRowByIndexpath
book = load_workbook(DataExcel)
def CreateFileCSV():
    df = pd.read_excel('new_big_file.xlsx','Left Member',index_col= None)
    dfCount = df.shape
    ARLefl = DicAndCsvExell('new_big_file.xlsx','Left Member',dfCount[0])
    ArGenneral = DicAndCsvExell('new_big_file.xlsx','General Member',dfCount[0])
    ARRight = DicAndCsvExell('new_big_file.xlsx','Right Member',dfCount[0])
    ValueChangeL = dict(zip(ValueChangeLeft_Right,ARLefl))
    ValueArGenneral = dict(zip(ValueGeneral,ArGenneral))
    ValueChangeR = dict(zip(ValueChangeLeft_Right,ARRight))
    ValueChangeL.update(ValueArGenneral)
    ValueChangeLSorted =  (sorted (ValueChangeL.items()))
    df = pd.DataFrame(dict(ValueChangeLSorted))
    for cols in df.columns:
        value = df.loc[1, cols]
        df[cols].fillna(value, inplace = True) 
    df.to_csv('Left.csv',index=False,header= False)
CreateFileCSV()