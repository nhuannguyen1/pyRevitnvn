from Autodesk.Revit.DB import FamilySymbol
import rpw
doc = rpw.revit.doc 
def FamilySymbolAtive (FamilySymbol):
 if FamilySymbol.IsActive == False:
	        FamilySymbol.Activate()
	        doc.Regenerate()