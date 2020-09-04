from Autodesk.Revit.DB import FilteredElementCollector,Family
import os,rpw,xlrd
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document

from pyrevitnvn.param import (set_param_from_symbol,
                              get_value_name
                              )
from pyrevitnvn.str import pro_str

from pyrevitnvn.draw import draw

dir_path = os.path.dirname(os.path.abspath(__file__))
filename = "Set_Config.csv"
path_conf = os.path.join(dir_path,filename)

@draw(filename=path_conf)
def run():

    opro_str = pro_str(path_conf)

    keys_Arr = opro_str.keys

    le_dict = opro_str.dic_in_arr()

    print (keys_Arr,le_dict)

    for index, edict in enumerate(le_dict):

        collectors = [vt for vt in FilteredElementCollector(doc).OfClass(Family)\
                      if vt.Name == edict.get(keys_Arr[0])
                      ]

        for collector in collectors:

            for sym_id in collector.GetFamilySymbolIds():

                symbol = doc.GetElement(sym_id) 

                Name_Value = get_value_name(symbol,
                                            edict,
                                            index,
                                            path_conf
                                            )
                set_param_from_symbol(symbol,edict.get(keys_Arr[1]),Name_Value)

run() 