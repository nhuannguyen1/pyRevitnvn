import os
import csv
#from Csv_Connect_Data import DataCSV
dir_path = os.path.dirname(os.path.realpath(__file__))
from ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
Config_Setting_Path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\Data_CSV\Config_Setting - Copy.csv'
path_Cof = ReturnDataAllRowByIndexpath(Config_Setting_Path,36)
Right_Genneral_All_path =os.path.join(path_Cof[0],'Right_Genneral_All.csv')
Left_Genneral_All_path =os.path.join(path_Cof[0],'Left_Genneral_All.csv')
DataExcel = os.path.join(dir_path,'DataALL - Template.xlsx')