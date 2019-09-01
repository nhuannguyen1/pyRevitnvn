__doc__ = 'Training Revit At Itivs '
__author__ = 'Nguyen Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,BuiltInParameter,\
Grid,SetComparisonResult,IntersectionResultArray,UnitUtils,DisplayUnitType,\
GlobalParametersManager,DoubleParameterValue,FamilyInstance
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Creation.Document import NewFamilyInstance
from pyrevit import script, forms
import clr
import rpw
import csv
import System
from GlobalParameter2 import Global,ConvertToInternalUnits1,GetParameterFromSubElement,setparameterfromvalue
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
Raffter_List = []
Raffter_List1 = []
import csv
#Get Family Symbol

def PlaceElement (Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled,Slope_Type,Level_Rater_Type_Lefted,Rater_Type_Lefted,Getcondination,LEVEL_ELEV_Base_Level,Length_Rater_Lefted):
    t = Transaction (doc,"Place Element")
    t.Start()
    ColumnCreate = doc.Create.NewFamilyInstance(Base_Leveled_Point, Column_Typed,Base_Leveled, Structure.StructuralType.NonStructural)
    LIST = GetParameterFromSubElement(ColumnCreate,Slope_Type)
    #H_n = GetParameterFromSubElement(ColumnCreate,'H_n').AsDouble()
    #H_n_Slope = GetParameterFromSubElement(ColumnCreate,'Slope')
    a= Global(Slope_Type)
    a.globalparameterchange(ColumnCreate)
    paramerTopLeve = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM)
    paramerTopLeve.Set(Top_Leveled.Id)
    TopoffsetPam = ColumnCreate.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM)
    TopoffsetPam.Set(0)

    H_t = LIST[1]
    H_n = LIST[0]

    Point_Level =XYZ (Getcondination.X + H_n,Getcondination.Y, H_t)

    PlaceElementRafter(Level_Rater_Type_Lefted,Point_Level,Rater_Type_Lefted,Slope_Type,Length_Rater_Lefted)
    t.Commit()
def PlaceElementRafter (Base_Leveled,Base_Leveled_Point,ELementsymbol,Slope_Type,Length_Rater_Lefted):
    Elementinstance = doc.Create.NewFamilyInstance(Base_Leveled_Point, ELementsymbol,Base_Leveled, Structure.StructuralType.NonStructural)
    a= Global(Slope_Type)
    a.globalparameterchange(Elementinstance)
    
    setparameterfromvalue(Elementinstance,'Length',Length_Rater_Lefted)
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
        self.Level_Rater_Type_Left.DataContext = self.levels
        # content connection
        #self.Plate_Connection_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Connections"]
        #content rater 
        self.Rafter_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Framing"]
    def ok_Click (self, sender, e):
        Column_Lefted = self.Column_Left.SelectedItem
        self.Column_Type.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).OfClass(FamilySymbol) if vt.FamilyName == Column_Lefted.Name]
        #content contection 
        #Plate_Connection_Lefted = self.Plate_Connection_Left.SelectedItem
        #self.Plate_Connection_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfClass(FamilySymbol) if vt.FamilyName == Plate_Connection_Lefted.Name]
        #content rater 
        Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
        self.Rater_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilySymbol) if vt.FamilyName == Rafter_Family_Lefted.Name]
    
    def Ok_Next(self, sender, e):
   
        Cout_Continue = int(self.InputNumberLeft.Text)
        self.InputNumberLeft.Text =str(Cout_Continue + 1)
        Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
        Rafter_Type_Lefted = self.Rater_Type_Left.SelectedItem
        #length 
        Length_Rater_Lefted_n = float(self.Length_Rater_Left.Text)
        print (Length_Rater_Lefted_n)
        # = UnitUtils.ConvertToInternalUnits(Length_Rater_Lefted_n, DisplayUnitType.DUT_MILLIMETERS)

        chuoi1 = str(Cout_Continue) + ',' + str(Rafter_Family_Lefted.Name) + ',' + str(Element.Name.__get__(Rafter_Type_Lefted)) + ',' + str(Length_Rater_Lefted_n) 

        t = Transaction(doc, 'Write an external file.')
        t.Start()
        #Set the file path
        filepath = r'D:\sometext.csv'
        #Delete the file if it exists.
        if (System.IO.File.Exists(filepath) == True):
            System.IO.File.Delete(filepath)
        #Create the file
        file = System.IO.StreamWriter(filepath)
        #Write some things to the file
        file.WriteLine(chuoi1)
        #Close the StreamWriter
        file.Close()
        t.Commit()

    def Ok_Prevous(self, sender, e):
        Cout_Prevous = int(self.InputNumberLeft.Text)
        self.InputNumberLeft.Text =str(Cout_Prevous - 1)
    def Click_To_Start(self, sender, e):  
        Base_Leveled = self.Base_Level.SelectedItem
        Top_Leveled = self.Top_Level.SelectedItem
        Gird_Vered = self.Gird_Ver.SelectedItem
        Gird_Hored = self.Gird_Hor.SelectedItem
        Column_Typed =self.Column_Type.SelectedItem
        Rater_Type_Lefted = self.Rater_Type_Left.SelectedItem
        Level_Rater_Type_Lefted =self.Level_Rater_Type_Left.SelectedItem
        LEVEL_ELEV_Base_Level= Top_Leveled.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
        #LEVEL_ELEV_Base_Level = UnitUtils.ConvertToInternalUnits(LEVEL_ELEV_Base_Level, DisplayUnitType.DUT_MILLIMETERS)
        Getcondination =  Getintersection (Gird_Vered.Curve,Gird_Hored.Curve)
        Base_Leveled_Point =XYZ (Getcondination.X,Getcondination.Y,(LEVEL_ELEV_Base_Level))
        # create slope 
        Slope_T = float(self.Slope.Text)
        #Create length 
        Length_Rater_Lefted = float(self.Length_Rater_Left.Text)
        Length_Rater_Lefted = UnitUtils.ConvertToInternalUnits(Length_Rater_Lefted, DisplayUnitType.DUT_MILLIMETERS)
        # place column to project 
        PlaceElement(Base_Leveled,Base_Leveled_Point,Column_Typed,Top_Leveled,Slope_T,Level_Rater_Type_Lefted,Rater_Type_Lefted,Getcondination,LEVEL_ELEV_Base_Level,Length_Rater_Lefted)
        #plate Element rafter 
        self.Close()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()