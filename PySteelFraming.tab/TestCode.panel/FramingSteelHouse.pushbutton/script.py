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
from GlobalParameter17 import Global,ConvertToInternalUnits1,GetParameterFromSubElement,\
    setparameterfromvalue,writefilecsv,Getcontentdata,count_csv,Return_Row,GetDataFirstRow,GetcontentdataStr,InputDataChangeToCSV,DataFromCSV
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
from pyrevit import script
import csv

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
        Column_Lefted = self.Column_Left.SelectedItem
        Column_Typed = self.Column_Type.SelectedItem
        Base_Leveled =self.Base_Level.SelectedItem
        Top_Leveled =self.Top_Level.SelectedItem
        Rafter_Family_Lefted = self.Rafter_Left.SelectedItem
        Rafter_Type_Lefted = self.Rater_Type_Left.SelectedItem
        Plate_Pted = float(self.Plate_Pt.Text)
        # Plate_Pted = self.Plate_Pt.SelectedItem
        LevelRafter = self.Level_Rater_Type_Left.SelectedItem
        Length_Rater_Lefted_n = self.Length_Rater_Left.Text
        Gird_Vered = self.Gird_Ver.SelectedItem
        Gird_Hored = self.Gird_Hor.SelectedItem
        Sloped = float(self.Slope.Text)
        if count_dem == 0 or Count_Continue >= count_dem:
            DataFromCSV_1 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            DataFromCSV_1.writefilecsv(count_dem)
        else:
            DataFromCSV_2 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            Return_Row1 =DataFromCSV_2.Return_Row()
            print (Return_Row1)
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            DataFromCSV_DATA = DataFromCSV(Count_Continue + 1,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            arr = DataFromCSV_DATA.Getcontentdata()
            #print (arr)  
            self.Column_Left.SelectedItem = arr[1]
            self.Column_Type.SelectedItem = arr[2]
            self.Base_Level.SelectedItem = (arr[3])
            self.Top_Level.SelectedItem = arr[4]
            self.Rafter_Left.SelectedItem = arr[5]
            self.Rater_Type_Left.SelectedItem = (arr[6])
            self.Level_Rater_Type_Left.SelectedItem = (arr[7])
            self.Length_Rater_Left.Text = str(arr[8])
            self.Plate_Pt.Text = str(arr[9])
            self.Gird_Hor.SelectedItem = (arr[11])
            self.Gird_Ver.SelectedItem =  (arr[12])
            self.Slope.Text =  str(arr[13])
            #print (Count_Continue)
            #Return_RowData = GetcontentdataStr(Count_Continue,path)
            DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            DataFromCSV_DATA.InputDataChangeToCSV(Return_Row1)
            #InputDataChangeToCSV(Count_Continue,path,Return_Row1)
        self.InputNumberLeft.Text = str (int(Count_Continue + 1))        
    def Ok_Prevous(self, sender, e):
        Cout_Prevous = int(self.InputNumberLeft.Text)
        self.InputNumberLeft.Text =str(Cout_Prevous - 1)
        arr = Getcontentdata(Cout_Prevous,path)
        self.Column_Type.DataContext = arr[1]
        self.Level_Rater_Type_Left.DataContext = arr[2]
        self.Length_Rater_Left.Text = str(arr[3])
    def Click_To_Start(self, sender, e):
            DataFromdem = DataFromCSV(int(0),None,None,None,None,None,None,None,None,None,path,None,None,None)
            arr = DataFromdem.Getcontentdata()
            dem = DataFromdem.count_csv()
      
            DataFromdem = DataFromCSV(int(0),arr[1],arr[2],(arr[3]),arr[4], arr[5],arr[6],arr[7],str(arr[8]),str(arr[9]),path,(arr[11]),(arr[12]),arr[13])
       
            t = Transaction (doc,"Place Element")
            t.Start()
            CreateColumn = DataFromdem.PlaceElement()
            DataFromdem.PlaceElementRafterFather(CreateColumn)
            t.Commit()
            #def  __init__(self, Count, FamilyCol, FamilyColType,Base_Level_Col,Top_Level_Col,FamilyRafter,FamilyRafterType,LevelRafter,Length_Rafter,Thinkess_Plate,path,Gird1,Gird2,Slope):
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()