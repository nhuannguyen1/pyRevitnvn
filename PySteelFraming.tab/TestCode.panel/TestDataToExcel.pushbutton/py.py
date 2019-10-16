from Autodesk.Revit.DB import Element, FilteredElementCollector,FamilySymbol,XYZ,Structure,Family,Level,Grid
import rpw
import csv
from DirectoryPath import Path_Config_Setting
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
def GetElementByName(Count, NameElement,row):
    if str(Count) in ReturnDataAllRowByIndexpath(Path_Config_Setting,12):
        for vt in FilteredElementCollector(doc).OfClass(Family):
            if vt.Name == NameElement:
               vt_Element = vt 
               return vt_Element  
    elif  str(Count) in ReturnDataAllRowByIndexpath(Path_Config_Setting,13):
        for vt in FilteredElementCollector(doc).OfClass(FamilySymbol):
        #for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements():
            if (Element.Name.__get__(vt)  == NameElement) and vt.FamilyName in [str(row[1]),str(row[5])] :
                vt_Element = vt
                return vt_Element  
    elif str(Count) in ReturnDataAllRowByIndexpath(Path_Config_Setting,14):
        for vt in FilteredElementCollector(doc).OfClass(Level):
            if vt.Name == NameElement:
               vt_Element = vt 
               return vt_Element 
    elif str(Count) in ReturnDataAllRowByIndexpath(Path_Config_Setting,15):
        for vt in FilteredElementCollector(doc).OfClass(Grid):
            try: 
                NameElement = int (NameElement)
                if vt.Name == str(NameElement):
                    vt_Element = vt 
                    return vt_Element  
            except:    
                if vt.Name == NameElement:
                    vt_Element = vt 
                    return vt_Element  
    else:
        vt_Element = NameElement
        return vt_Element  
def ReturnDataAllRowByIndexpath (path,NumberRow):
        with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=',')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        del RowNumber[0]
        return RowNumber