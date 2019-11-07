from openpyxl.styles import Alignment
from ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
from Path_Connect_Excel import Right_Genneral_All_path,Left_Genneral_All_path,DataExcel,Config_Setting_Path

ValueGeneral = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,22)]
#remove Column move 
#Columnmove = ReturnDataAllRowByIndexpath(Config_Setting_Path,32)
Columnmove = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,32)]

LocationCellForMoveColumn = ReturnDataAllRowByIndexpath(Config_Setting_Path,34)

ArrRangMax = [* range(max([int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,22)] + Columnmove + [int(i) for i in  ReturnDataAllRowByIndexpath(Config_Setting_Path,0)]) + 1)]

ValueChangeLeft_Right  = set(ArrRangMax).difference(set(ValueGeneral + Columnmove))

IndexChangeRemoveColumn = set([int(i) for i in  ReturnDataAllRowByIndexpath(Config_Setting_Path,0)]).difference(set(Columnmove))

GenneralColumnNotChange =  [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,38)]

GeneralConcernRaffter = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,40)]

Genneral_Select = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,42)]

LocationOfRowLeft = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,46)]

LocationOfRowRight = [int(i) for i in ReturnDataAllRowByIndexpath(Config_Setting_Path,48)]

ExcelCellForMoveColumnRight = ReturnDataAllRowByIndexpath(Config_Setting_Path,50)

def HandlingDataSTr (Element):
    Element1 = Element.replace(":",",")
    Element2= Element1.replace("(","")
    Element3= Element2.replace(")","")
    return eval(Element3)
def GetIndexOfNotChange(IndexChange,IndexChangeTotal):
    IndexArr =  [IndexChangeTotal.index(indexc) for indexc in IndexChange]
    return  IndexArr
def AligntText(sheet):
    rows = range(1, 500)
    columns = range(1, 44)
    for row in rows:
        for col in columns:
            sheet.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)