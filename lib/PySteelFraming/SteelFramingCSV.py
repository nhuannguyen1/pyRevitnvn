import csv
Conf_set_path = r'C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\GetDataFromColumnAndFraming.panel\GetDataFromColumnAndFraming.pushbutton\Set_Config.csv'
from PySteelFraming.ReturnDataAllRowByIndexpath import ReturnDataAllRowByIndexpath
Arr_characters_special = ReturnDataAllRowByIndexpath(Conf_set_path,1)
KeepValueNotChange = ReturnDataAllRowByIndexpath(Conf_set_path,0)
def ReturnDataAllRowByIndexpathAll ():
    with open(Conf_set_path) as csvFile:
        readcsv =csv.reader(csvFile, delimiter=';')
        readcsv = list(readcsv)
        #RowNumber = readcsv[1]
    csvFile.close()
    return readcsv
ArrReturn = ReturnDataAllRowByIndexpathAll()
keys = ArrReturn[2]
def Handling_DataS_Tr (Arr_Index_Element,Arr):
    Arr_Index_Element = list(func(Arr_Index_Element))
    Arr_Element = [Arr[(vt[0]+1):(vt[1])] for vt in Arr_Index_Element]
    Arr_Element = list(dict.fromkeys(Arr_Element))
    if "" in Arr_Element:
        Arr_Element.remove("")
    return (Arr_Element)
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
    for i in range(3,len(ArrReturn),1):
        values = ArrReturn[i]
        Handling_Element= Handling_Data_Element(values)
        dictionary = dict(zip(keys, Handling_Element))
        dictionary_Arr.append(dictionary)
    print ("dictionary_Arr",dictionary_Arr)
    return dictionary_Arr