import re
from Autodesk.Revit.DB import (XYZ,
                                Line,
                                Grid,
                                BuiltInParameter,
                                Transaction
                                ) 
                        
from pyrevitnvn.hexcel import dby_Lindex_col
                                
from pyrevitnvn.units import Convert_length
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document   

def dgrid(name_text_gird_col = "A", 
            dist_gird_col = "B", 
            length_gird_col = "C", 
            coord_start = (0,0,0),
            type_d = "vertical",
            sheet = None
            ):
    """
    create grid to project \n
    name_text_gird_col: colum index from  excel to retrieve text gird \n
    dist_gird_col: distance of gird \n
    length_gird_col: length of gird \n
    """
    # create dict from range 
    dicta = dby_Lindex_col(sheet=sheet,
                           key_index_column=name_text_gird_col,
                           value_index_cols=[dist_gird_col,length_gird_col])

    # sort list by number 
    lkey = sorted(list(dicta.keys()),key=lambda x: int((re.findall('\d+', x ))[0]))

    # check verical or horzontal 
    c = coord_start[0] if type_d == "vertical" else coord_start[1] 

    # retrieve of all distance 
    sum_total_dis = Convert_length(sum ([dicta[key][0]  for key in lkey ]))

    # drawing gird x vertical 
    for key in lkey:
        # retrieve distance and length 
        dis,length = dicta[key]

        # convert unit for dis
        dis = Convert_length(dis)
        
        # convert unit for length
        length = Convert_length(length) if type(length)== float else sum_total_dis

        dis = c + dis
        
        if type_d == "vertical":
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

        # context-like objects that guard any 
        # changes made to a Revit model
        t = Transaction(doc, "Create grids")

        # Starts the transaction.
        t.Start()

        # create line reference 
        line_ref = Line.CreateBound(scoord, ecoord)

        # create gird  
        grid_ins = Grid.Create(doc, line_ref)

        # retrieve name for gird 
        name = grid_ins.get_Parameter(BuiltInParameter.DATUM_TEXT)

        # set name for gird 
        name.Set(key)

        # Commits all changes made 
        # to the model during the transaction.
        t.Commit()
def d2grid(ver_name_text_gird_col = "A", 
           ver_dist_gird_col = "B", 
           ver_length_gird_col = "C", 
           ver_coord_start = (0,0,0),
           hor_name_text_gird_col = "A", 
           hor_dist_gird_col = "B", 
           hor_length_gird_col = "C", 
           hor_coord_start = (0,0,0),
            sheet = None
            ):
    """
    create grid to project \n
    name_text_gird_col: colum index from  excel to retrieve text gird \n
    dist_gird_col: distance of gird \n
    length_gird_col: length of gird \n
    """
    # create dict from range 
    dicta = dby_Lindex_col(sheet=sheet,
                           key_index_column=name_text_gird_col,
                           value_index_cols=[dist_gird_col,length_gird_col])

    # sort list by number 
    lkey = sorted(list(dicta.keys()),key=lambda x: int((re.findall('\d+', x ))[0]))

    # check verical or horzontal 
    c = coord_start[0] if type_d == "vertical" else coord_start[1] 

    # retrieve of all distance 
    sum_total_dis = Convert_length(sum ([dicta[key][0]  for key in lkey ]))

    # drawing gird x vertical 
    for key in lkey:
        # retrieve distance and length 
        dis,length = dicta[key]

        # convert unit for dis
        dis = Convert_length(dis)
        
        # convert unit for length
        length = Convert_length(length) if type(length)== float else sum_total_dis

        dis = c + dis
        
        if type_d == "vertical":
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

        # context-like objects that guard any 
        # changes made to a Revit model
        t = Transaction(doc, "Create grids")

        # Starts the transaction.
        t.Start()

        # create line reference 
        line_ref = Line.CreateBound(scoord, ecoord)

        # create gird  
        grid_ins = Grid.Create(doc, line_ref)

        # retrieve name for gird 
        name = grid_ins.get_Parameter(BuiltInParameter.DATUM_TEXT)

        # set name for gird 
        name.Set(key)

        # Commits all changes made 
        # to the model during the transaction.
        t.Commit()