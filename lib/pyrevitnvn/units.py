from Autodesk.Revit.DB import (UnitType,
                                UnitUtils,
                                ) 
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document                        
def Convert_length(length):
    """ 
    convert  length To Internal Units \n
    Converts a value from a given display unit to Revit's internal units.
    """
    # retrieve unit display current in revit 
    unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
    display_unit = unit_format_options.DisplayUnits
    return UnitUtils.ConvertToInternalUnits(float(length), display_unit)

def Convert_From_Internal_Display_Length(length):
    """ 
    convert  length To Internal Units \n
    Converts a value from a given display unit to Revit's internal units.
    """
    # retrieve unit display current in revit 
    unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
    display_unit = unit_format_options.DisplayUnits
    return UnitUtils.ConvertFromInternalUnits (float(length), display_unit)

def Convert_Display_length_To_Internal(length):
    """ 
    convert  length To Internal Units \n
    Converts a value from a given display unit to Revit's internal units.
    """
    # retrieve unit display current in revit 
    unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)
    display_unit = unit_format_options.DisplayUnits
    return UnitUtils.ConvertToInternalUnits(float(length), display_unit)