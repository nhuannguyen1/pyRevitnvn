__doc__ = 'Training Revit At Itivs '
__author__ = 'Nguyen Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,BuiltInParameter,\
Grid,SetComparisonResult,IntersectionResultArray,UnitUtils,DisplayUnitType,\
GlobalParametersManager,DoubleParameterValue
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Creation.Document import NewFamilyInstance
from pyrevit import script, forms
import clr
import rpw
from GlobalParameter4 import Global,ConvertToInternalUnits1
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert

#Get Family Symbol

def PlaceElement (Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled,Slope_Type,XYZConnection,ConnectionType):
    t = Transaction (doc,"Place Element")
    t.Start()
    #ColumnCreate = doc.Create.NewFamilyInstance(XYZConnection, ConnectionType,XYZ_Direction,Element_Host, Structure.SNonStructural)
    ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, Column_Typed,Base_Leveled, Structure.StructuralType.Column)
    a= Global(Slope_Type)

    

    a.globalparameterchange(ColumnCreate)
    paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
    paramerTopLeve.Set(Top_Leveled.Id)
    TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
    TopoffsetPam.Set(0)
    
    print (ColumnCreate)
    CreateElementHost (XYZConnection, ConnectionType,ColumnCreate)

    t.Commit()

def CreateElementHost(XYZConnection, ConnectionType,element_Host):
    #t = Transaction (doc,"Place Element host")
    #t.Start()
    ConectionPlate = doc.Create.NewFamilyInstance(XYZConnection, ConnectionType, element_Host, Structure.StructuralType.NonStructural)
    """
    a= Global(Slope_Type)
    a.globalparameterchange(ColumnCreate)
    paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
    paramerTopLeve.Set(Top_Leveled.Id)
    TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
    TopoffsetPam.Set(0)
    """
   # t.Commit()
   
def Getintersection (line1, line2):
    results = clr.Reference[IntersectionResultArray]()
    result = line1.Intersect(line2, results)
    if result != SetComparisonResult.Overlap:
	    print('No Intesection')
    res = results.Item[0]
    return res.XYZPoint
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
        # content connection
        self.Plate_Connection_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Connections"]
        #content rater 
        self.Rafter_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Framing"]
    def ok_Click (self, sender, e):
        Column_Lefted = self.Column_Left.SelectedItem
        self.Column_Type.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).OfClass(FamilySymbol) if vt.FamilyName == Column_Lefted.Name]
        #content contection 
        Plate_Connection_Lefted = self.Plate_Connection_Left.SelectedItem
        self.Plate_Connection_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfClass(FamilySymbol) if vt.FamilyName == Plate_Connection_Lefted.Name]
        #content rater 
        Rater_Type_Lefted = self.Rafter_Left.SelectedItem
        self.Rater_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilySymbol) if vt.FamilyName == Rater_Type_Lefted.Name]
    def Click_To_Start(self, sender, e):  
        Base_Leveled = self.Base_Level.SelectedItem
        Top_Leveled = self.Top_Level.SelectedItem
        Gird_Vered = self.Gird_Ver.SelectedItem
        Gird_Hored = self.Gird_Hor.SelectedItem
        Column_Typed =self.Column_Type.SelectedItem
        LEVEL_ELEV_Base_Level= Top_Leveled.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        LEVEL_ELEV_Base_Level = UnitUtils.ConvertToInternalUnits(LEVEL_ELEV_Base_Level, DisplayUnitType.DUT_MILLIMETERS)
        Getcondination =  Getintersection (Gird_Vered.Curve,Gird_Hored.Curve)
        Base_Leveled_Point =XYZ (Getcondination.X,Getcondination.Y,(LEVEL_ELEV_Base_Level))
        # create slope 
        Slope_T = float(self.Slope.Text)

        Plate_Connection_Type_Lefted = self.Plate_Connection_Type_Left.SelectedItem
        print (Plate_Connection_Type_Lefted)
        XYZConnection = XYZ (2,2,2)
        # place column to project 
        PlaceElement(Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled,Slope_T,XYZConnection,Plate_Connection_Type_Lefted)
        #plate Element to host 
       

        self.Close()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()