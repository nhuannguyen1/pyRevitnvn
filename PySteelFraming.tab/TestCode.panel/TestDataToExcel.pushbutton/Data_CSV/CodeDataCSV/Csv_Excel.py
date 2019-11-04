from openpyxl.styles import Alignment
def HandlingDataSTr (Element):
    Element1 = Element.replace(":",",")
    Element2= Element1.replace("(","")
    Element3= Element2.replace(")","")
    return eval(Element3)
def GetIndexOfNotChange(IndexChange,IndexChangeTotal):
    IndexArr =  [IndexChangeTotal.index(indexc) for indexc in IndexChange]
    return  IndexArr
def AligntText(sheet):
    rows = range(1, 44)
    columns = range(1, 44)
    for row in rows:
        for col in columns:
            sheet.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)