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
    setparameterfromvalue,DataFromCSV,CheckTypeLengthBal,CheckSelectedValueForFamily,CheckSelectedValueForFamilyType
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
from pyrevit import script
import csv
from System import Array
import xlsxwriter 
import excel
path_excel = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\ExcelTest8.xlsx"
import xlrd 
#get Config in revit 
path = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\TestDataToExcel.pushbutton\ExcelTest1.csv"

#Open workbook and Get data from Sheet 

ex = excel.initialise()
ex.Visible = True
workbook = ex.Workbooks.Open(path_excel)
sheet = workbook.Sheets("Sheet1")
#lr = sheet.Range("A" + Rows.Count).End(xlUp).Row
lr = excel.FindLastRowOFData(sheet)
print ("lr",lr)
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
        self.Gird_Ver_G.DataContext = self.Girds
        #self.Gird_Hor_G.DataContext = self.Girds
        self.Level_Rater_Type_Left.DataContext = self.levels
        DataFromdem = DataFromCSV(1,None,None,None,None,None,None,None,None,None,path,None,None,None,None,None,None,None)
        #DataFromdem.DeleteRow()
        GetDataFirst = DataFromdem.GetContentDataFromExcel(workbook)
        #print (GetDataFirst[3].Name,GetDataFirst[4].Name)
        self.Column_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[1])
        self.Column_Type.SelectedValue = CheckSelectedValueForFamilyType(GetDataFirst[2])
        self.Base_Level.SelectedValue  = CheckSelectedValueForFamily(GetDataFirst[3])
        self.Top_Level.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[4])
        self.Rafter_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[5])
        self.Rater_Type_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[6])
        self.Level_Rater_Type_Left.SelectedValue = CheckSelectedValueForFamilyType(GetDataFirst[7])
        self.Length_Rater_Left.Text = str(GetDataFirst[8])
        self.Plate_Pt.Text = str(GetDataFirst[9])
        self.Gird_Hor.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[11])
        self.Gird_Ver.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[12])
        self.Slope.Text = str(GetDataFirst[13])
        self.Gird_Ver_G.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[14])
        self.Gird_Hor_G.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[15])
        self.Length_From_Gird.Text = str(GetDataFirst[16])
        self.Plate_Column.Text = str(GetDataFirst[17])
    def Reset_Data(self, sender, e):
        DataFromdem = DataFromCSV(0,None,None,None,None,None,None,None,None,None,path,None,None,None,None,None,None,None)
        DataFromdem.DeleteRow()
        self.InputNumberLeft.Text = str (0)
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
    def Changed_Grid(self, sender, e):
        try:
            self.ChangedGrid = sender.SelectedItem
            self.Gird_Hor.DataContext =[vt for vt in FilteredElementCollector(doc).OfClass(Grid) if vt.Name != self.ChangedGrid.Name]
        except:
            pass    
    def Changed_Grid_R(self, sender, e):
        try:
            self.ChangedGrid = sender.SelectedItem
            self.Gird_Hor_G.DataContext =[vt for vt in FilteredElementCollector(doc).OfClass(Grid) if vt.Name != self.ChangedGrid.Name]
        except:
            pass   
    def Ok_Next(self, sender, e):
        Count_Continue = int(self.InputNumberLeft.Text)

        DataFromdem = DataFromCSV(None,None,None,None,None,None,None,None,None,None,path,None,None,None,None,None,None,None)
        #count_dem = DataFromdem.count_csv()
        count_dem = excel.FindLastRowOFData(sheet)
        #print ("count_dem is and Continue  ",count_dem , Count_Continue)
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
        Gird_Ver_Ged = self.Gird_Ver_G.SelectedItem
        Gird_Hor_Ged = self.Gird_Hor_G.SelectedItem
        Length_From_Girded = float(self.Length_From_Gird.Text)
        Plate_Columned = float(self.Plate_Column.Text)
        if count_dem == 0 or Count_Continue > (count_dem-1):
            #print ("Rafter_Family_Lefted dem 0" ,Rafter_Family_Lefted)  
            DataFromCSV_1 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
            DataFromCSV_1.writefilecsv(Count_Continue,sheet)
        else:
            #print ("Rafter_Family_Lefted dem 1" ,Rafter_Family_Lefted)
            DataFromCSV_2 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
            Return_Row1 =DataFromCSV_2.Return_Row()
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            if (Count_Continue == (count_dem - 1)):
                DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                    Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,\
                        Gird_Vered,Sloped,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
                arr = DataFromCSV_DATA.GetContentDataFromExcel(sheet)
            else:
                DataFromCSV_DATA = DataFromCSV(Count_Continue + 1,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                    Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,\
                        Gird_Vered,Sloped,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
                arr = DataFromCSV_DATA.GetContentDataFromExcel(sheet)
            self.Column_Left.SelectedValue = CheckSelectedValueForFamily(arr[1])
            self.Column_Type.SelectedValue = CheckSelectedValueForFamilyType(arr[2])
            self.Base_Level.SelectedValue = CheckSelectedValueForFamily(arr[3])

            self.Top_Level.SelectedValue = CheckSelectedValueForFamily(arr[4])

            self.Rafter_Left.SelectedValue = CheckSelectedValueForFamily(arr[5])
            self.Rater_Type_Left.SelectedValue = CheckSelectedValueForFamilyType(arr[6])
            self.Level_Rater_Type_Left.SelectedValue = CheckSelectedValueForFamily(arr[7])
            self.Length_Rater_Left.Text = str(arr[8])
            self.Plate_Pt.Text = str(arr[9])
            self.Gird_Hor.SelectedValue = CheckSelectedValueForFamily(arr[11])
            self.Gird_Ver.SelectedValue = CheckSelectedValueForFamily(arr[12])
            self.Slope.Text =  str(arr[13])
            self.Gird_Ver_G.SelectedValue =  CheckSelectedValueForFamily(arr[14])
            self.Gird_Hor_G.SelectedValue = CheckSelectedValueForFamily(arr[15])
            self.Length_From_Gird.Text = str(arr[16])
            self.Plate_Column.Text =str(arr[17])
            DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped,Gird_Ver_Ged,\
                    Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
            DataFromCSV_DATA.InputDataChangeToCSV(Return_Row1)
        self.InputNumberLeft.Text = str (int(Count_Continue + 1))     
    def Ok_Prevous(self, sender, e):
            DataFromdem = DataFromCSV(None,None,None,None,None,None,None,None,None,None,path,None,None,None,None,None,None,None)
            count_dem = DataFromdem.count_csv()
            Count_Continue = int(self.InputNumberLeft.Text)
        #try:
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
            Gird_Ver_Ged = self.Gird_Ver_G.SelectedItem
            Gird_Hor_Ged = self.Gird_Hor_G.SelectedItem
            Length_From_Girded = float(self.Length_From_Gird.Text)
            Plate_Columned = float(self.Plate_Column.Text)
            DataFromCSV_2 = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped,Gird_Ver_Ged,\
                    Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
            Return_Row1 =DataFromCSV_2.Return_Row()
            #Return_Row1 = Return_Row(Count_Continue,Rafter_Family_Lefted,Rafter_Type_Lefted,Length_Rater_Lefted_n)
            DataFromCSV_DATA = DataFromCSV(Count_Continue -1,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,\
                Rafter_Family_Lefted,Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,\
                    Gird_Vered,Sloped,Gird_Ver_Ged,Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
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

            self.Gird_Ver_G.SelectedValue =  (arr[14]).Name
            self.Gird_Hor_G.SelectedValue = (arr[15]).Name
            self.Length_From_Gird.Text = str(arr[16])
            self.Plate_Column.Text =str(arr[17])

            DataFromCSV_DATA = DataFromCSV(Count_Continue,Column_Lefted,Column_Typed,Base_Leveled,Top_Leveled,Rafter_Family_Lefted,\
                Rafter_Type_Lefted,LevelRafter,Length_Rater_Lefted_n,Plate_Pted,path,Gird_Hored,Gird_Vered,Sloped,Gird_Ver_Ged,\
                    Gird_Hor_Ged,Length_From_Girded,Plate_Columned)
            if count_dem == Count_Continue:
                self.InputNumberLeft.Text = str (int(Count_Continue - 1))
            else:
                DataFromCSV_DATA.InputDataChangeToCSV(Return_Row1)
                self.InputNumberLeft.Text = str (int(Count_Continue - 1))
    def Click_To_Start(self, sender, e):
            DataFromdem = DataFromCSV(int(0),None,None,None,None,None,None,None,None,None,path,None,None,None,None,None,None,None)
          
            arr = DataFromdem.Getcontentdata()
            #dem = DataFromdem.count_csv()
            DataFromdem = DataFromCSV(int(0),arr[1],arr[2],(arr[3]),arr[4], arr[5],arr[6],arr[7],str(arr[8]),\
                str(arr[9]),path,(arr[11]),(arr[12]),arr[13],(arr[14]),(arr[15]),arr[16],arr[17])
            t = Transaction (doc,"Place Element")
            t.Start()
            CreateColumn = DataFromdem.PlaceElement()
            DataFromdem.PlaceElementRafterFather(CreateColumn)
            t.Commit()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog() 