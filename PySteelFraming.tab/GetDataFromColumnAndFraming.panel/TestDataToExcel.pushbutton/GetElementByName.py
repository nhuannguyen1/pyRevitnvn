from Autodesk.Revit.DB import Element, FilteredElementCollector,FamilySymbol,XYZ,Structure,Family,Level,Grid
import rpw
import csv
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
class ElementName:
    def  __init__(self, path = None):
        self.path = path
    def GetElementByName(self,Count, NameElement,row):
        #StrArrCount = [row[int(vt)] for vt in ReturnDataAllRowByIndexpath(Path_Config_Setting,12)]
        #print (StrArrCount)
        if str(Count) in ReturnDataAllRowByIndexpath(self.path,12):
            for vt in FilteredElementCollector(doc).OfClass(Family):
                if vt.Name == NameElement:
                    vt_Element = vt 
                    return vt_Element  
        elif  str(Count) in ReturnDataAllRowByIndexpath(self.path,13):
            for vt in FilteredElementCollector(doc).OfClass(FamilySymbol):
            #for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements():
            #if (Element.Name.__get__(vt)  == NameElement) and vt.FamilyName in [str(row[1]),str(row[5]),str(row[27])] :
                StrArrCount = [row[int(vtc)] for vtc in ReturnDataAllRowByIndexpath(self.path,12)]
                if (Element.Name.__get__(vt)  == NameElement) and vt.FamilyName in StrArrCount:
                    vt_Element = vt
                    return vt_Element  
        elif str(Count) in ReturnDataAllRowByIndexpath(self.path,14):
            for vt in FilteredElementCollector(doc).OfClass(Level):
                if vt.Name == NameElement:
                    vt_Element = vt 
                    return vt_Element 
        elif str(Count) in ReturnDataAllRowByIndexpath(self.path,15):
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
