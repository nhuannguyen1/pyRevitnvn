# coding: utf8

import System

from Autodesk.Revit.DB import Document, UnitUtils, UnitType, UnitSymbolType, LabelUtils, FormatOptions, DisplayUnitType

import rpw
from pyrevit import forms, script

doc = rpw.revit.doc  # type: Document

unit_format_options = doc.GetUnits().GetFormatOptions(UnitType.UT_Length)


display_unit = unit_format_options.DisplayUnits
symbol_type = unit_format_options.UnitSymbol
if symbol_type == UnitSymbolType.UST_NONE:
    try:
        symbol_type = FormatOptions.GetValidUnitSymbols(display_unit).Item[1]
    except System.ArgumentOutOfRangeException:
        display_unit = DisplayUnitType.DUT_DECIMAL_FEET
        symbol_type = FormatOptions.GetValidUnitSymbols(display_unit).Item[1]
symbol = LabelUtils.GetLabelFor(symbol_type)

def import_config_length(length):
    return str(UnitUtils.ConvertFromInternalUnits(float(length), display_unit))

def export_config_length(lenght):
    return str(UnitUtils.ConvertToInternalUnits(float(lenght), display_unit))

class CreateSectionOptions(forms.WPFWindow):
    def __init__(self):
        forms.WPFWindow.__init__(self, "CreateSectionOptions.xaml")
        #self.set_image_source(self.diagram_img, "diagram.png")

        #self.tblock_units.Text = "All length in {}".format(symbol)

        # get parameters from config file or use default values
        self._config = script.get_config()

        self.X_Top.Text = import_config_length(self._config.get_option('X_Top_X', '1'))
        self.X_Bottom.Text = import_config_length(self._config.get_option('X_Bottom_X', '1'))
        self.X_Left.Text = import_config_length(self._config.get_option('X_Left_X', '1'))
        self.X_Right.Text = import_config_length(self._config.get_option('X_Right_X', '1'))

    def save_options(self, sender, e):
        self._config.X_Top_X = export_config_length(self.X_Top.Text)
        self._config.X_Bottom_X = export_config_length(self.X_Bottom.Text)
        self._config.X_Left_X = export_config_length(self.X_Left.Text)
        self._config.X_Right_X = export_config_length(self.X_Right.Text)
        script.save_config()
        self.Close()
    def reset_options(self, sender, e):
        script.reset_config()
        self.Close()
        reseted_gui = CreateSectionOptions().show_dialog()

options_gui = CreateSectionOptions().show_dialog()

