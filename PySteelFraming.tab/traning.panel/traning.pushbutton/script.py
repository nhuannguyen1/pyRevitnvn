__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Test Code'
# Import commom language runtime
import xlrd
import string
import re
# Import commom language runtime
# Import Revit API
from Autodesk.Revit.DB import (Transaction,
                                UnitType,
                                UnitUtils,
                                XYZ,
                                Line,
                                Grid,
                                BuiltInParameter
                                ) 
                        
from Autodesk.Revit.UI.Selection import  ObjectType 
from Autodesk.Revit.Creation.ItemFactoryBase import NewDimension
import os
def col2num(col):
    """Return number corresponding to excel-style column."""
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def Convert_length(length):
    """ 
    convert  length To Internal Units \n
    Converts a value from a given display unit to Revit's internal units.
    """
    # retrieve unit display current in revit 
    unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
    display_unit = unit_format_options.DisplayUnits
    return UnitUtils.ConvertToInternalUnits(float(length), display_unit)

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
    return [sheet.cell_value(row,col2num(index_col)-1)\
            for row in range(start_row,sheet.nrows)\
            if sheet.cell_value(row,col2num(index_col) - 1)\
            != value_ignore
            ]

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
    key = LbyRange(sheet=sheet,
                    index_col=key_index_column
                    )
    return dict(zip(key, dvalue))

def dgird(name_text_gird = "A", 
            dist_gird_col = 2000, 
            length_gird_col = 300, 
            coord_start = (0,0,0),
            type = "vertical"
            ):
    # create dict from range 
    dicta = dby_Lindex_col(sheet=sheet,
                        key_index_column=name_text_gird,
                        value_index_cols=[dist_gird_col,length_gird_col])
    #dictb = dby_Lindex_col(sheet=sheet,key_index_column="D",value_index_cols=[dist_gird,length_gird])
    lkey = sorted(list(dicta.keys()),key=lambda x: int((re.findall('\d+', x ))[0]))

    c = coord_start[0] if type == "vertical" else coord_start[1] 
    # drawing gird x vertical 
    for key in lkey:
        # retrieve distance and length 
        dis,length = dicta[key]
        # convert unit for dis
        dis = Convert_length(dis)
        # convert unit for distance
        length = Convert_length(length)
        dis = c + dis
        if type == "vertical":
            # coord start 
            scoord = XYZ(dis,0,0)
            # coord start 
            ecoord = XYZ(dis,length,0)
        else:
            # coord start 
            scoord = XYZ(0,dis,0)
            # coord start 
            ecoord = XYZ(length,dis,0)
        c= dis
        # create line reference 
        line_ref = Line.CreateBound(scoord, ecoord)
        # create gird  
        grid_ins = Grid.Create(doc, line_ref)
        # retrieve name for gird 
        name = grid_ins.get_Parameter(BuiltInParameter.DATUM_TEXT)
        # set name for gird 
        name.Set(key)
# Import Revit API
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
# retrieve dir path from fullname 
dir_path = os.path.dirname(os.path.abspath(__file__))
# retrieve directory excel file 
file_loc =os.path.join(dir_path,"Create_Grids.xlsx")
# open wb by xlrd 
workbook = xlrd.open_workbook(filename=file_loc)
# retrieve sheet excel  by index
sheet = workbook.sheet_by_index(0)

t = Transaction(doc, "Dimension grids")

Origin_Coordx = eval(sheet.cell_value(0,1))

Origin_Coordy = eval(sheet.cell_value(0,4))

t.Start()
dgird(name_text_gird="D",
        dist_gird_col="E",
        length_gird_col="F",
        type="horizontal",
        coord_start=Origin_Coordy
        )
dgird(name_text_gird="A",
        dist_gird_col="B",
        length_gird_col="C",
        coord_start=Origin_Coordx
        )
t.Commit()
