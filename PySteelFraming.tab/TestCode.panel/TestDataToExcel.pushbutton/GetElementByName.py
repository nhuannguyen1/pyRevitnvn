from Autodesk.Revit.DB import Element, FilteredElementCollector,FamilySymbol,XYZ,Structure,Family,Level,Grid
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
def GetElementByName(Count, NameElement):
    if any(str(Count) in s for s in [str(1),str(5)]):
        for vt in FilteredElementCollector(doc).OfClass(Family):
            if vt.Name == NameElement:
               vt_Element = vt 
               return vt_Element  
    elif  any(Count in s for s in [str(2),str(6)]):
        for vt in FilteredElementCollector(doc).OfClass(FamilySymbol):
        #for vt in FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements():
            if Element.Name.__get__(vt)  == NameElement:
                vt_Element = vt
                return vt_Element  
    elif any(Count in s for s in [str(3),str(4),str(7)]):
        for vt in FilteredElementCollector(doc).OfClass(Level):
            if vt.Name == NameElement:
               vt_Element = vt 
               return vt_Element 
    elif any(Count in s for s in [str(11),str(12),str(14),str(15)]):
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