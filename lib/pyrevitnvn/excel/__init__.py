import xlrd

def evalifcan(leval = ""):
    
    return leval.split(",") if "," in leval else leval

def eval_list_except(list_eval = [],ex_ele_index = [3]):
    newleval = []
    for index,ele in enumerate(list_eval):
        if index in ex_ele_index :
            newleval.append(ele)
        else:
            newleval.append(ele.split(",") if "," in ele else ele )
    return newleval


def lvalue_by_index_row(sheet,start_row,is_value_to_fill_out = False):

    """ 
    return list value by index row
    """
    ar = [(sheet.cell_value(r, c)) for c in range(sheet.ncols) for r in range(start_row,start_row + 1)]

    return eval_list_except(list_eval=ar)

def dic_in_arr(path = None, 
               index_row_key = 3, 
               index_row_value_start = 4
               ):
    """ 
    create list inclue dicts 
    """
    # get workbook 
    book = xlrd.open_workbook(path)
    # get sheet by index 
    sheet = book.sheet_by_index(0)
    # get value key 
    data = lvalue_by_index_row(sheet,index_row_key)
    lvaluek = []
    for i in range(index_row_value_start,sheet.nrows) :

        dele = dict(zip(data,
                        lvalue_by_index_row(sheet,
                                            i,
                                            is_value_to_fill_out= True
                                            )
                        )
                    )
        lvaluek.append(dele)
    return lvaluek