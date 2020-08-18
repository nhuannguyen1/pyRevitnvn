__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Test Code'
# Import commom language runtime
import xlrd
# Import commom language runtime
# Import Revit API
from pynvn.excel import col2num
import os

# retrieve dir path from fullname 
dir_path = os.path.dirname(os.path.abspath(__file__))
# retrieve directory excel file 
file_loc =os.path.join(dir_path,"Create_Grids.xlsx")
# open wb by xlrd 
workbook = xlrd.open_workbook(file_loc)
# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)
def LbyRange (sheet = None, 
                index_col = "A", 
                value_ignore = ["",None],
                start_row = 2
                ):
    """ 
    return list by range excel \n
    sheet: worksheet input \n
    index_col: index of column to create list from col_index
    """
    Lrow = [sheet.cell_value(row,col2num(index_col)-1) for row in range(start_row,sheet.nrows) if sheet.cell_value(row,col2num(index_col) - 1) != value_ignore]
    return Lrow

def dby_Lindex_col (sheet = None, 
                key_index_column = "A", 
                value_index_cols = ["B","C"],
                value_ignore = ["",None],
                start_row = 2
                ):
    dvalue =  [[sheet.cell_value(row,col2num(index_col)-1)\
                for index_col in value_index_cols]\
                for row  in range(start_row,sheet.nrows)\
                if  sheet.cell_value(row,col2num(key_index_column)-1)\
                not in value_ignore 
                ]
        
    key = LbyRange(sheet=sheet,index_col="A")
    
    return dict(zip(key, dvalue))
print (dby_Lindex_col(sheet=sheet))

