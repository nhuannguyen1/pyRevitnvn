import string
def col2num(col):
    """
    Return number corresponding to excel-style column \n
    ex: A--->1,B--->2 
    """
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num
    
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
    """ 
    Retrieve dict from range index colum \n
    key_index_column: key index column \n
    value_index_cols:  retrieve value from excel \n
    start_row: row to start 
    """


    try: 
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
    except:
        return	{}