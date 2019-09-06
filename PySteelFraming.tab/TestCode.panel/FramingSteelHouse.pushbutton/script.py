__doc__ = 'Training Revit At Itivs '
__author__ = 'Nguyen Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,Element,XYZ,Structure,Family,Level,BuiltInParameter,\
Grid,SetComparisonResult,IntersectionResultArray,UnitUtils,DisplayUnitType,\
GlobalParametersManager,DoubleParameterValue,FamilyInstance,ElementId
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Creation.Document import NewFamilyInstance
from pyrevit import script, forms
import clr
import rpw
from GlobalParameter1 import Global,ConvertToInternalUnits1,GetParameterFromSubElement,\
    setparameterfromvalue,writefilecsv,Getcontentdata,count_csv,Return_Row,GetDataFirstRow,GetcontentdataStr,InputDataChangeToCSV,DataFromCSV
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
from pyrevit import script
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
#path = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PyRevitNVN.extension\PyRevitNVN.tab\TextCodePython.panel\Text.pushbutton\sometext.csv"
path = r"C:\Users\nhuan.nguyen\Desktop\sometext.csv"
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
        #  # get parameters from config file or use default values
        
        self._config = script.get_config()
        inputNumber = GetDataFirstRow(path)
        self.Rafter_Left.Text = self._config.get_option('prefix', inputNumber[1])
        self.Rater_Type_Left.Text = self._config.get_option('prefix', inputNumber[2])
        self.Length_Rater_Left.Text = self._config.get_option('prefix', inputNumber[3])
        
        self._config.prefix = self.Length_Rater_Left.Text
        self._config.prefix = self.Rafter_Left.Text
        self._config.prefix = self.Rater_Type_Left.Text
        # content connection
        #self.Plate_Connection_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Connections"]
        #content rater 
        self.Rafter_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Framing"]
    def ok_Click (self, sender, e):
        Column_Lefted = self.Column_Left.SelectedItem
        self.Column_Type.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).OfClass(FamilySymbol) if vt.FamilyName == Column_Lefted.Name]
        Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
        self.Rater_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilySymbol) if vt.FamilyName == Rafter_Family_Lefted.Name]
    def Ok_Next(self, sender, e):
        Count_Continue = int(self.InputNumberLeft.Text)
        DataFromdem = DataFromCSV(None,None,None,None,None,None,None,None,None,None,path,None,None,None)
        count_dem = DataFromdem.count_csv()
        #count_dem = count_csv(path)
        if count_dem == 0 or Count_Continue >= count_dem:
            #add
            Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
            Rafter_Type_Lefted = self.Rater_Type_Left.SelectedItem
            Length_Rater_Lefted_n = float(self.Length_Rater_Left.Text)
            DataFromCSV_1 = DataFromCSV(Count_Continue,None,None,None,None,Rafter_Family_Lefted,Rafter_Type_Lefted,None,Length_Rater_Lefted_n,None,path,None,None,None)
            DataFromCSV_1.writefilecsv(count_dem)
            #writefilecsv(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n,path,count_dem)
            self.InputNumberLeft.Text = str (int(Count_Continue + 1))
            self.InputNumberLeft_other.Text = str (Count_Continue)
        else:
            Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
            Rafter_Type_Lefted = self.Rater_Type_Left.SelectedItem
            Length_Rater_Lefted_n = float(self.Length_Rater_Left.Text)
            
            DataFromCSV_1 = DataFromCSV(Count_Continue,None,None,None,None,Rafter_Family_Lefted,Rafter_Type_Lefted,None,Length_Rater_Lefted_n,None,path,None,None,None)
            Return_Row1 =DataFromCSV_1.Return_Row()
            print (Return_Row1)
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            DataFromCSV_1 = DataFromCSV(Count_Continue + 1,None,None,None,None,Rafter_Family_Lefted,Rafter_Type_Lefted,None,Length_Rater_Lefted_n,None,path,None,None,None)
            arr = DataFromCSV_1.Getcontentdata()
            print (arr)
            #arr = Getcontentdata ((Count_Continue + 1),path)
            self.Column_Type.DataContext = arr[1]
            self.Level_Rater_Type_Left.DataContext = arr[2]
            self.Length_Rater_Left.Text = str(arr[3])
            
            #print (Count_Continue)
            #Return_RowData = GetcontentdataStr(Count_Continue,path)
            DataFromCSV_1 = DataFromCSV(Count_Continue,None,None,None,None,Rafter_Family_Lefted,Rafter_Type_Lefted,None,Length_Rater_Lefted_n,None,path,None,None,None)
            DataFromCSV_1.InputDataChangeToCSV(Return_Row1)
            #InputDataChangeToCSV(Count_Continue,path,Return_Row1)
            self.InputNumberLeft.Text = str (int(Count_Continue + 1))
            self.InputNumberLeft_other.Text = str (Count_Continue)
    def Ok_Prevous(self, sender, e):
        Cout_Prevous = int(self.InputNumberLeft.Text)
        self.InputNumberLeft.Text =str(Cout_Prevous - 1)
        arr = Getcontentdata(Cout_Prevous,path)
        self.Column_Type.DataContext = arr[1]
        self.Level_Rater_Type_Left.DataContext = arr[2]
        self.Length_Rater_Left.Text = str(arr[3])
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