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
from GlobalParameter2 import Global,ConvertToInternalUnits1,GetParameterFromSubElement,\
    setparameterfromvalue,writefilecsv,Getcontentdata,count_csv,Return_Row,GetDataFirstRow,GetcontentdataStr,InputDataChangeToCSV,DataFromCSV
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
from pyrevit import script
import csv

path = r"C:\Users\nhuan.nguyen\Desktop\sometext.csv"
class WPF_PYTHON(WPFWindow):
    def __init__(self, xaml_file_name):
     
        WPFWindow.__init__(self, xaml_file_name)
        self.Column_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Columns"]
        self.Rafter_Left.DataContext =  [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Framing"]
        self.levels = FilteredElementCollector(doc).OfClass(Level)
        self.Base_Level.DataContext = self.levels
        self.Top_Level.DataContext = self.levels
        self.Girds = FilteredElementCollector(doc).OfClass(Grid)
        self.Gird_Ver.DataContext = self.Girds
        self.Gird_Hor.DataContext = self.Girds
        self.Level_Rater_Type_Left.DataContext = self.levels
        
        DataFromdem = DataFromCSV(0,None,None,None,None,None,None,None,None,None,path,None,None,None)
        count_dem = DataFromdem.count_csv()
        if count_dem !=  0:
            GetDataFirst = DataFromdem.Getcontentdata()
            #print (GetDataFirst[3].Name,GetDataFirst[4].Name)
            self.Column_Left.SelectedValue = GetDataFirst[1].Name
            self.Column_Type.SelectedValue = Element.Name.__get__(GetDataFirst[2])
            self.Base_Level.SelectedValue  = GetDataFirst[3].Name
            self.Top_Level.SelectedValue = GetDataFirst[4].Name
            self.Rafter_Left.SelectedValue = GetDataFirst[5].Name

            self.Rater_Type_Left.SelectedValue = Element.Name.__get__(GetDataFirst[6])
            self.Level_Rater_Type_Left.SelectedValue = GetDataFirst[7].Name
            self.Length_Rater_Left.Text = str(GetDataFirst[8])
            self.Plate_Pt.Text = str(GetDataFirst[9])
            self.Gird_Hor.SelectedValue = (GetDataFirst[11]).Name
            self.Gird_Ver.SelectedValue = (GetDataFirst[12]).Name
            self.Slope.Text = str(GetDataFirst[13])

    def source_Family_selection_changed(self, sender, e):
        try:
            self.Column_Left_SD = sender.SelectedItem
            self.Column_Type.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).OfClass(FamilySymbol) if vt.FamilyName ==  self.Column_Left_SD.Name]
        except:
             pass
    def source_Type_selection_changed(self, sender, e):
        try:
            self.Rafter_Left_SD = sender.SelectedItem
            self.Rater_Type_Left.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilySymbol) if vt.FamilyName == self.Rafter_Left_SD.Name]
        except:
            pass
          
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
    
        if count_dem == 0 or Count_Continue > (count_dem-1):
            DataFromCSV_1 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            DataFromCSV_1.writefilecsv(count_dem)
        else:
            DataFromCSV_2 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            Return_Row1 =DataFromCSV_2.Return_Row()
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            if (Count_Continue == (count_dem - 1)):
                DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                    Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
                arr = DataFromCSV_DATA.Getcontentdata()
            else:
                DataFromCSV_DATA = DataFromCSV(Count_Continue + 1,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                    Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
                arr = DataFromCSV_DATA.Getcontentdata()
            self.Column_Left.SelectedValue = arr[1].Name
            self.Column_Type.SelectedValue = Element.Name.__get__(arr[2])
            self.Base_Level.SelectedValue = arr[3].Name

            self.Top_Level.SelectedValue = arr[4].Name
            self.Rafter_Left.SelectedValue = arr[5].Name
            self.Rater_Type_Left.SelectedValue = Element.Name.__get__(arr[6])
            self.Level_Rater_Type_Left.SelectedValue = arr[7].Name
            self.Length_Rater_Left.Text = str(arr[8])
            self.Plate_Pt.Text = str(arr[9])
            self.Gird_Hor.SelectedValue = (arr[11]).Name
            self.Gird_Ver.SelectedValue = (arr[12]).Name
            self.Slope.Text =  str(arr[13])
            DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            DataFromCSV_DATA.InputDataChangeToCSV(Return_Row1)
        self.InputNumberLeft.Text = str (int(Count_Continue + 1))        
    def Ok_Prevous(self, sender, e):
        Count_Continue = int(self.InputNumberLeft.Text)
        try:
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
            DataFromCSV_2 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            Return_Row1 =DataFromCSV_2.Return_Row()
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            DataFromCSV_DATA = DataFromCSV(Count_Continue -1,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            arr = DataFromCSV_DATA.Getcontentdata()
            self.Column_Left.SelectedValue = arr[1].Name
            self.Column_Type.SelectedValue = Element.Name.__get__(arr[2])
            self.Base_Level.SelectedValue = arr[3].Name
            self.Top_Level.SelectedValue = arr[4].Name
            self.Rafter_Left.SelectedValue = arr[5].Name
            self.Rater_Type_Left.SelectedValue = Element.Name.__get__(arr[6])
            self.Level_Rater_Type_Left.SelectedValue = arr[7].Name
            self.Length_Rater_Left.Text = str(arr[8])
            self.Plate_Pt.Text = str(arr[9])
            self.Gird_Hor.SelectedValue = (arr[11]).Name
            self.Gird_Ver.SelectedValue = (arr[12]).Name
            self.Slope.Text =  str(arr[13])
            DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped)
            DataFromCSV_DATA.InputDataChangeToCSV(Return_Row1)
            self.InputNumberLeft.Text = str (int(Count_Continue - 1))
        except:
             print("Unable to retrieve reference level from this object")

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
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()