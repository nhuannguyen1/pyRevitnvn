import pandas as pd
def DicAndCsvExell(NameExelFile,SheetName,Count):
    df = pd.read_excel(NameExelFile,SheetName,index_col= None)
    dfCount = df.shape
    CountInput = Count + 1 - dfCount[0]
    df = pd.concat([df]*CountInput, ignore_index=True)
    AR =  [df.columns.values.tolist()] + df.values.tolist()
    AR1 = list(zip(*AR[::1]))
    return AR1
def Update_Dict_Joint(*List):
    Genenral_Dict = {} 
    for subDict in List:
        Genenral_Dict.update(subDict)
        Genenral_Dict_Sorted = (sorted (Genenral_Dict.items()))
        Genenral_Dict_Sorted = dict(Genenral_Dict_Sorted)
    return Genenral_Dict_Sorted
