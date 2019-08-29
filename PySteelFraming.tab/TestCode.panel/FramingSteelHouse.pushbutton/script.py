__doc__ = 'Training Revit At Itivs '
__author__ = 'Nguyen Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,BuiltInParameter,Grid,SetComparisonResult,IntersectionResultArray,UnitUtils,DisplayUnitType,GlobalParametersManager,DoubleParameterValue
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Creation.Document import NewFamilyInstance
from pyrevit import script, forms
import clr
import rpw
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
#Get Family Symbol

def PlaceElement (Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled):
    t = Transaction (doc,"Place Element")
    t.Start()
    ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, Column_Typed,Base_Leveled, Structure.StructuralType.Column)
    paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
    paramerTopLeve.Set(Top_Leveled.Id)
    TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
    TopoffsetPam.Set(0)
    t.Commit()
def Getintersection (line1, line2):
    results = clr.Reference[IntersectionResultArray]()
    result = line1.Intersect(line2, results)
    if result != SetComparisonResult.Overlap:
	    print('No Intesection')
    res = results.Item[0]
    return res.XYZPoint
def ConvertToInternalUnits(UNIT):
    ParameterValue = UnitUtils.ConvertToInternalUnits(UNIT, DisplayUnitType.DUT_MILLIMETERS)
    return ParameterValue
def GlobalParameter():
    t = Transaction (doc,"Slope Element")
    t.Start()
    paramId = GlobalParametersManager.FindByName(doc, "Slope")
    param = doc.GetElement(paramId) 
    paramtype = type(param)
    ParameterValue = UnitUtils.ConvertToInternalUnits(20, DisplayUnitType.DUT_DECIMAL_DEGREES)
    param.SetValue (DoubleParameterValue(ParameterValue))
    t.Commit()
class WPF_PYTHON(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.Column_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Columns"]
        self.levels = FilteredElementCollector(doc).OfClass(Level)
        self.Base_Level.DataContext = self.levels
        self.Top_Level.DataContext = self.levels
        
        self.Girds = FilteredElementCollector(doc).OfClass(Grid)
        self.Gird_Ver.DataContext = self.Girds
        self.Gird_Hor.DataContext = self.Girds


        #self.Column_Type1 =self.Column_Left1.OfClass(FamilySymbol)
        #self.Column_Type.DataContext =self.Column_Type1
    def ok_Click (self, sender, e):
        Column_Lefted = self.Column_Left.SelectedItem
        GlobalParameter ()
        self.Column_Type.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).OfClass(FamilySymbol) if vt.FamilyName == Column_Lefted.Name]
    def Click_To_Start(self, sender, e):  
        Base_Leveled = self.Base_Level.SelectedItem
        Top_Leveled = self.Top_Level.SelectedItem
        print (Top_Leveled)
        LEVEL_ELEV_Base_Level= Top_Leveled.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        LEVEL_ELEV_Base_Level = UnitUtils.ConvertToInternalUnits(LEVEL_ELEV_Base_Level, DisplayUnitType.DUT_MILLIMETERS)
        Gird_Vered = self.Gird_Ver.SelectedItem
        Gird_Hored = self.Gird_Hor.SelectedItem

        Getcondination =  Getintersection (Gird_Vered.Curve,Gird_Hored.Curve)

        Base_Leveled_Point =XYZ (Getcondination.X,Getcondination.Y,(LEVEL_ELEV_Base_Level))

        Column_Typed =self.Column_Type.SelectedItem
        PlaceElement(Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled)
        self.Close()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()
