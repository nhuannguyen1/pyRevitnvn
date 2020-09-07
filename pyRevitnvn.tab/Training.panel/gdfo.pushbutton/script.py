__doc__ = 'Set value for parameter'
__author__ = 'pyan.vn'
__title__ = 'Gdfo'
from Autodesk.Revit.DB import (FilteredElementCollector,
                               Family
                               )
import os,rpw,xlrd

uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

from pyrevitnvn.param import (set_param_from_symbol,
                              get_value_name
                              )
from pyrevitnvn.str import pro_str

from pyrevitnvn.draw import draw

from pyrevitnvn.excel import (lvalue_by_index_row,
                              dic_in_arr
                              )

# retrieve dir path from abspath 
dir_path = os.path.dirname(os.path.abspath(__file__))

# retrieve fullname excel file 
path_conf = os.path.join(dir_path,"ex_conf.xlsx")

@draw(filename=path_conf)
def run():
    # return dict in list from excel 
    le_dict = dic_in_arr(path=path_conf,
                         index_row_key=3,
                         index_row_value_start=4
                         )
    for index, edict in enumerate(le_dict):
        # list value key 
        keys = sorted(edict.keys())
        # filter family project by name family in list excel 
        collectors = [vt for vt in FilteredElementCollector(doc).OfClass(Family)\
                      if vt.Name == edict.get(keys[0])
                      ]
        for collector in collectors:
            for sym_id in collector.GetFamilySymbolIds():
                # get family symbol from id 
                symbol = doc.GetElement(sym_id)
                # get new name to input to parameter
                name_value = get_value_name(symbol,
                                            edict,
                                            index
                                            )

                #set parameter value to
                set_param_from_symbol(symbol,edict.get(keys[1]),name_value)
                
run() 