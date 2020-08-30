from pyrevitnvn.units import Convert_From_Internal_Display_Length
import re
def dictfrompara(ele,
                 para_names
                 ):
    return {para_name :Convert_From_Internal_Display_Length(ele.LookupParameter(para_name).AsDouble()) for para_name in para_names}

def typename_from_data(instr = "",
                 ele = None,
                 pattern = 'x|mm'
                 ):

    listparam = list(filter(lambda x: x !="",re.split(pattern, instr)))
    dictele = dictfrompara(ele=ele,
                           para_names=listparam
                           ) 

    for param_name in listparam:

        instr = instr.replace(param_name,str(dictele[param_name]))

    return instr

def pattern_by_user(pattern = "I-W.(|-|x|F.|)x|,"):
    """
    pattern_by_user 
    add  \ to pattern 
    """
    lspec  = list("[]{^$*+?}()")
    for char in lspec:
        if char in pattern:
            print(char)
            pattern = pattern.replace(char,"\{0}".format(char))
            pattern = pattern.replace('\\\\', '\\')
            print ("patternin",pattern)
    return pattern