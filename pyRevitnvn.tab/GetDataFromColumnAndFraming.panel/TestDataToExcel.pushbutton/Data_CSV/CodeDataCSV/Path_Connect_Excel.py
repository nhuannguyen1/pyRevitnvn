import os
import csv
#from Csv_Connect_Data import DataCSV
dir_path = os.path.dirname(os.path.realpath(__file__))
Config_Setting_Path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\GetDataFromColumnAndFraming.panel\TestDataToExcel.pushbutton\Data_CSV\Config_Setting.csv'
path_Cof = os.path.dirname(Config_Setting_Path)
Right_Genneral_All_path =os.path.join(path_Cof,'Right_Genneral_All.csv')
Left_Genneral_All_path =os.path.join(path_Cof,'Left_Genneral_All.csv')
DataExcel = os.path.join(dir_path,'DataALL - Template.xlsx')