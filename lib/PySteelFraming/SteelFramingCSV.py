import csv
Conf_Set_Path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\GetDataFromColumnAndFraming.panel\GetDataFromColumnAndFraming.pushbutton\Set_Config.csv'
from ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
Arr_characters_special = ReturnDataAllRowByIndexpath(Conf_Set_Path,1)
KeepValueNotChange = ReturnDataAllRowByIndexpath(Conf_Set_Path,0)
Check_Con_To_Case_Expect  = ReturnDataAllRowByIndexpath(Conf_Set_Path,2)
def ReturnDataAllRowByIndexpathAll ():
    with open(Conf_Set_Path) as csvFile:
        readcsv =csv.reader(csvFile, delimiter=';')
        readcsv = list(readcsv)
    csvFile.close()
    return readcsv
ArrReturn = ReturnDataAllRowByIndexpathAll()
keys = ArrReturn[3]
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
def Handling_DataS_Tr (Arr_Index_Element,Arr):
    Arr_Index_Element = list(func(Arr_Index_Element))
    Arr_Element = [Arr[(vt[0]+1):(vt[1])] for vt in Arr_Index_Element]
    Arr_Element_El = Remove(Arr_Element)
    #Arr_Element = list(dict.fromkeys(Arr_Element))
    if "" in Arr_Element_El:
        Arr_Element_El.remove("")
    return (Arr_Element_El)
def func(alist):
    return zip(alist, alist[1:])
def Handling_Data_Element(Arr_Elements):
    Handling_DataS_Tr_Ap = []
    for index_Arr,Arr_Element in enumerate(Arr_Elements,0):
        Arr_Index_Element = [index for index,vt in enumerate(Arr_Element,0) if vt in Arr_characters_special]
        Handling_DataS_Tr_eD = Handling_DataS_Tr(Arr_Index_Element,Arr_Element)
        if str(index_Arr) in KeepValueNotChange:
            Handling_DataS_Tr_Ap.append(Arr_Element)
        else:
            Handling_DataS_Tr_Ap.append(Handling_DataS_Tr_eD)  
    return Handling_DataS_Tr_Ap
def CreateDict():
    dictionary_Arr = []
    for i in range(4,len(ArrReturn),1):
        values = ArrReturn[i]
        Handling_Element= Handling_Data_Element(values)
        dictionary = dict(zip(keys, Handling_Element))
        dictionary_Arr.append(dictionary)
    return dictionary_Arr
def Handling_DataS_Tr_For_Case_Expect():
    Handling_DataS_Tr_For_Case_Expected = []
    for ElementStr in Check_Con_To_Case_Expect:
        Arr_Index_Element = [index for index,vt in enumerate(ElementStr,0) if vt in Arr_characters_special]
        Value_Check_For_For_Case_Expect = Handling_DataS_Tr(Arr_Index_Element,ElementStr)
        Handling_DataS_Tr_For_Case_Expected.append(Value_Check_For_For_Case_Expect)
    return Handling_DataS_Tr_For_Case_Expected
Handling_DataS_Tr_For_Case_Expect()