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

def create_gird(scoord,
                ecoord,
                name_gird
                ):
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
    name.Set(name_gird)

    # Commits all changes made 
    # to the model during the transaction.
    t.Commit()

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
                           value_index_cols=[dist_gird_col,length_gird_col]
                           )

    # sort list by number 
    lkey = sorted(list(dicta.keys()),
                  key=lambda x: int((re.findall('\d+', x ))[0])
                  )

    # check verical or horzontal 
    c = coord_start[0] if type_d == "vertical" else coord_start[1] 

    # retrieve of all distance 
    sum_total_dis = Convert_length(sum ([dicta[key][0] for key in lkey ]))

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
            # coord start X
            scoord = XYZ(dis,0,0)
            # coord start X
            ecoord = XYZ(dis,length,0)
        else:
            # coord start Y
            scoord = XYZ(0,dis,0)
            # coord start Y
            ecoord = XYZ(length,dis,0)

        c= dis

        # drawing gird to project 
        create_gird(scoord=scoord,
                    ecoord=ecoord,
                    name_gird=key
                    )

def d2grid(ver_name_text_gird_col = "A", 
           ver_dist_gird_col = "B", 
           ver_length_gird_col = "C", 
           ver_coord_start = (0,0,0),
           hor_name_text_gird_col = "D", 
           hor_dist_gird_col = "E", 
           hor_length_gird_col = "F", 
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
    ver_dicta = dby_Lindex_col(sheet=sheet,
                               key_index_column=ver_name_text_gird_col,
                               value_index_cols=[ver_dist_gird_col,ver_length_gird_col])

    # sort list by number 
    ver_lkey = sorted(list(ver_dicta.keys()),
                      key=lambda x: int((re.findall('\d+', x ))[0]))

    # check verical or horzontal 
    ver_c = Convert_length(ver_coord_start[0])

    # retrieve of all distance 
    ver_sum_total_dis = Convert_length(sum ([ver_dicta[key][0] for key in ver_lkey ]))

    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # create dict from range 
    hor_dicta = dby_Lindex_col(sheet=sheet,
                               key_index_column=hor_name_text_gird_col,
                               value_index_cols=[hor_dist_gird_col,hor_length_gird_col]
                               )
    # sort list by number 
    hor_lkey = sorted(list(hor_dicta.keys()),
                      key=lambda x: int((re.findall('\d+', x ))[0]))

    # check verical or horzontal 
    hor_c = Convert_length(hor_coord_start[1])

    # retrieve of all distance 
    hor_sum_total_dis = Convert_length(sum ([hor_dicta[key][0]  for key in hor_lkey ]))
    #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # drawing gird x vertical 
    for key in ver_lkey:
        # retrieve distance and length 
        dis,length = ver_dicta[key]

        # convert unit for dis
        dis = Convert_length(dis)
        
        # convert unit for length
        length = Convert_length(length) if type(length)== float else hor_sum_total_dis + Convert_length(hor_coord_start[1])

        dis = ver_c + dis

        # coord start 
        scoord = XYZ(dis,0,0)

        # coord end 
        ecoord = XYZ(dis,length,0)

        ver_c= dis
        # drawing gird to project 
        create_gird(scoord=scoord,
                ecoord=ecoord,
                name_gird=key
                )

    for key in hor_lkey:
        # retrieve distance and length 
        dis,length = hor_dicta[key]

        # convert unit for dis
        dis = Convert_length(dis)
        
        # convert unit for length
        length = Convert_length(length) if type(length)== float else ver_sum_total_dis + Convert_length(ver_coord_start[0])

        dis = hor_c + dis
        
        # coord start 
        scoord = XYZ(0,dis,0)
        
        # coord end
        ecoord = XYZ(length,dis,0)
        
        hor_c= dis

        # drawing gird to project 
        create_gird(scoord=scoord,
                    ecoord=ecoord,
                    name_gird=key
                    )
