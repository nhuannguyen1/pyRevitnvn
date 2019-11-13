import rpw
from Autodesk.Revit.DB import UnitUtils,UnitType,DisplayUnitType
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
display_unit = unit_format_options.DisplayUnits
symbol_type = unit_format_options.UnitSymbol
def Convert_length(length):
    Int_Length = (UnitUtils.ConvertFromInternalUnits(float(length), display_unit))
    return int(round(Int_Length))
