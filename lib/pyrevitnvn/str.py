from ReturnDataAllRowByIndexpath import PathSteel
class pro_str:
    """ 
    handling for  string
    """
    def  __init__(self, 
                  path = None
                  ):
        self.Return_Arr_Re = PathSteel(path)
        self.Arr_characters_special = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(1)
        self.KeepValueNotChange = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(0) 
        self.ArrReturn = self.Return_Arr_Re.ReturnDataAllRowByIndexpathAll()
        self.Check_Con_To_Case_Expect = self.Return_Arr_Re.ReturnDataAllRowByIndexpath(2)
        self.keys = self.ArrReturn[3]

    def Handling_Data_Tr (self,
                          Arr_Index_Element,
                          Arr
                          ):

        Arr_Index_Element = list(func(Arr_Index_Element))
        Arr_Element = [Arr[(vt[0]+1):(vt[1])] for vt in Arr_Index_Element]
        Arr_Element_El = Remove(Arr_Element)
        if "" in Arr_Element_El:
            Arr_Element_El.remove("")
        return (Arr_Element_El)

    def Handling_Data_Element(self,
                              Arr_Elements
                              ):

        Handling_DataS_Tr_Ap = []
        for index_Arr,Arr_Element in enumerate(Arr_Elements,0):
            Arr_Index_Element = [index for index,vt in enumerate(Arr_Element,0) if vt in self.Arr_characters_special]
            Handling_DataS_Tr_eD = self.Handling_Data_Tr(Arr_Index_Element,Arr_Element)
            if str(index_Arr) in self.KeepValueNotChange:
                Handling_DataS_Tr_Ap.append(Arr_Element)
            else:
             Handling_DataS_Tr_Ap.append(Handling_DataS_Tr_eD)  
        return Handling_DataS_Tr_Ap

    def dic_in_arr(self):
        """ 
        create arr include dict element

        """
        dictionary_Arr = []
        for i in range(4,len(self.ArrReturn),1):
            values = self.ArrReturn[i]
            Handling_Element= self.Handling_Data_Element(values)
            dictionary = dict(zip(self.keys, Handling_Element))
            dictionary_Arr.append(dictionary)
        return dictionary_Arr

    def Handling_DataS_Tr_For_Case_Expect(self):

        Handling_DataS_Tr_For_Case_Expected = []
        for ElementStr in self.Check_Con_To_Case_Expect:
            Arr_Index_Element = [index for index,vt in enumerate(ElementStr,0) if vt in self.Arr_characters_special]
            Value_Check_For_For_Case_Expect = self.Handling_Data_Tr(Arr_Index_Element,ElementStr)
            Handling_DataS_Tr_For_Case_Expected.append(Value_Check_For_For_Case_Expect)
        return Handling_DataS_Tr_For_Case_Expected

# remove Duplicate element from list 
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def func(alist):
    return zip(alist, alist[1:])

