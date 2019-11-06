import pandas as pd
def DicAndCsvExell(NameExelFile,SheetName,Count):
    df = pd.read_excel(NameExelFile,SheetName,index_col= None)
    dfCount = df.shape
    CountInput = Count + 1 - dfCount[0]
    df = pd.concat([df]*CountInput, ignore_index=True)
    AR =  [df.columns.values.tolist()] + df.values.tolist()
    AR1 = list(zip(*AR[::1]))
    return AR1
"""
def checkavalueexists(yourValue,df):
    for cols in df.columns:
    	if (yourValue in df[cols]:
		    print('Found in '+cols)
"""