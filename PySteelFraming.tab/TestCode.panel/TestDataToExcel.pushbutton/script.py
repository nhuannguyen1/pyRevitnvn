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
import os.path
import clr
import rpw
from GlobalParameter import setparameterfromvalue,DataFromCSV,CheckTypeLengthBal,\
    CheckSelectedValueForFamily,ArrFistForDefautValue_FC,CountNumberOfRow,\
        CountNumberOfColumn,writeRowTitle,GetPath,SynChronizeValueToCSV_T,GetPath_Right
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow, alert
from pyrevit import script
import csv
import os
def GetArrDataExcell(DataToolTemplate):
    #DataToolTemplate = GetPath()
    if os.stat(DataToolTemplate).st_size == 0:
        writeRowTitle()
    ArrDataExcell = ArrFistForDefautValue_FC()
    return ArrDataExcell
"""
DataToolTemplate = GetPath()
writeRowTitle1 = writeRowTitle()
if os.stat(DataToolTemplate).st_size == 0:
    writeRowTitle()
ArrDataExcell = ArrFistForDefautValue_FC()
count_dem = CountNumberOfRow() - 1
"""
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
        self.Level_Rater_Type_Left.DataContext = self.levels
        self.Select_Member.DataContext = ["Member Left","Member Right"]
        DataToolTemplate = GetPath()
        ArrDataExcell = GetArrDataExcell(DataToolTemplate)
        count_dem = CountNumberOfRow(DataToolTemplate) - 1
        self.SetValueFromContentData(ArrDataExcell,count_dem)
        """
        if count_dem != 0:
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            GetDataFirst = DataFromdem.GetContentDataFromExcel()
            self.GetValueOfSelectedValue(GetDataFirst)
        else:
            GetDataFirst = ArrDataExcell
            self.GetValueOfSelectedValue(GetDataFirst)
        """
    def SetValueFromContentData (self,ArrDataExcell,count_dem):
        if count_dem != 0:
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            GetDataFirst = DataFromdem.GetContentDataFromExcel()
            self.GetValueOfSelectedValue(GetDataFirst)
        else:
            GetDataFirst = ArrDataExcell
            self.GetValueOfSelectedValue(GetDataFirst)
    def Select_Member_changed(self, sender, e):
        self.Select_Member = sender.SelectedItem
        if self.Select_Member == "Member Left":
            DataToolTemplate = GetPath()
        elif self.Select_Member == "Member Right":
            DataToolTemplate = GetPath_Right() 
        else:
            print ("Pls check ")
        return DataToolTemplate
    def GetValueOfSelectedValue(self,GetDataFirst):
        self.Column_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[1])
        self.Column_Type.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[2])
        self.Base_Level.SelectedValue  = CheckSelectedValueForFamily(GetDataFirst[3])
        self.Top_Level.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[4])
        self.Rafter_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[5])
        self.Rater_Type_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[6])
        self.Level_Rater_Type_Left.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[7])
        self.Length_Rater_Left.Text = CheckSelectedValueForFamily((GetDataFirst[8]))
        self.Plate_Pt.Text = CheckSelectedValueForFamily((GetDataFirst[9]))
        self.path_excel = CheckSelectedValueForFamily((GetDataFirst[10]))
        self.Gird_Ver.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[11])
        self.Gird_Hor.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[12])
        self.Slope.Text = CheckSelectedValueForFamily((GetDataFirst[13]))
        self.Gird_Ver_G.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[14])
        self.Gird_Hor_G.SelectedValue = CheckSelectedValueForFamily(GetDataFirst[15])
        self.Length_From_Gird.Text = CheckSelectedValueForFamily((GetDataFirst[16]))
        self.Plate_Column.Text = CheckSelectedValueForFamily((GetDataFirst[17]))
        self.Move_Left.Text = CheckSelectedValueForFamily((GetDataFirst[18]))
        self.Move_Right.Text = CheckSelectedValueForFamily((GetDataFirst[19]))
        self.Move_Up.Text = CheckSelectedValueForFamily((GetDataFirst[20]))
        self.Move_Bottom.Text = CheckSelectedValueForFamily((GetDataFirst[21]))
        self.Offset_Top_Level.Text = CheckSelectedValueForFamily((GetDataFirst[22]))
    def Reset_Data(self, sender, e):
        #ArrDataExcell [0] = 1
        #ArrDataExcell [10] = DataToolTemplate
        DataToolTemplate = GetPath()
        ArrDataExcell = GetArrDataExcell(DataToolTemplate)
        DataFromdem = DataFromCSV(*ArrDataExcell)
        DataFromdem.Set_Count(1)
        DataFromdem.DeleteRowToReset()
        self.InputNumberLeft.Text = str (1)
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
    def ArraySelectedItemfs(self,Count_Continue):
        DataToolTemplate = GetPath()
        ArraySelectedItem = [Count_Continue,self.Column_Left.SelectedItem,self.Column_Type.SelectedItem,self.Base_Level.SelectedItem,\
            self.Top_Level.SelectedItem,self.Rafter_Left.SelectedItem,self.Rater_Type_Left.SelectedItem,\
                self.Level_Rater_Type_Left.SelectedItem,self.Length_Rater_Left.Text,float(self.Plate_Pt.Text),DataToolTemplate,self.Gird_Ver.SelectedItem,self.Gird_Hor.SelectedItem,\
                    float(self.Slope.Text),self.Gird_Ver_G.SelectedItem,self.Gird_Hor_G.SelectedItem,float(self.Length_From_Gird.Text),float(self.Plate_Column.Text),\
                        float(self.Move_Left.Text),float(self.Move_Right.Text),float(self.Move_Up.Text),float(self.Move_Bottom.Text),float(self.Offset_Top_Level.Text)]
        return ArraySelectedItem
    def Ok_Next(self, sender, e):
        try:
            Count_Continue = int(self.InputNumberLeft.Text)
            DataToolTemplate = GetPath()
            count_dem = CountNumberOfRow(DataToolTemplate) - 1
            if Count_Continue > (count_dem):
                a = Count_Continue
                ArraySelectedItem = self.ArraySelectedItemfs(a)
                ArraySelectedItem [0] = a
                #print ("Rafter_Family_Lefted dem 0" ,Rafter_Family_Lefted)  
                DataFromCSV_1 = DataFromCSV(*ArraySelectedItem)
                DataFromCSV_1.writefileExcel(Count_Continue)
            elif (Count_Continue == 1 and count_dem == 1):
                ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
                #print ("Rafter_Family_Lefted dem 1" ,Rafter_Family_Lefted)
                DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
                Return_Row1 =DataFromCSV_2.Return_Row_Excel()
                ArraySelectedItem [0] = Count_Continue 
                DataFromCSV_DATA = DataFromCSV(*ArraySelectedItem)
                arr = DataFromCSV_DATA.GetContentDataFromExcel()
                self.GetValueOfSelectedValue(arr)
                DataFromCSV_DATA.InputDataChangeToCSV_Excel(Return_Row1)
            else:
                ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
                #print ("Rafter_Family_Lefted dem 1" ,Rafter_Family_Lefted)
                DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
                Return_Row1 =DataFromCSV_2.Return_Row_Excel()
                if (int(Count_Continue) < int(count_dem)) or (int(Count_Continue) == 1):
                    ArraySelectedItem [0] = Count_Continue 
                    DataFromCSV_DATA = DataFromCSV(*ArraySelectedItem)
                    arr = DataFromCSV_DATA.GetContentDataFromExcel_Test2()
                    self.GetValueOfSelectedValue(arr)
                    DataFromCSV_DATA.InputDataChangeToCSV_Excel(Return_Row1)
            self.InputNumberLeft.Text = str (int(Count_Continue + 1))
        except  :
            print ("Check Ok_Next")
    def Ok_Prevous(self, sender, e):
        try:
            DataToolTemplate = GetPath()
            count_dem = CountNumberOfRow(DataToolTemplate)
            Count_Continue = int(self.InputNumberLeft.Text)
            if count_dem == Count_Continue:
                self.InputNumberLeft.Text = str (int(Count_Continue) - 1)
            else:
                ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
                #ArraySelectedItem[10] = DataToolTemplate
                DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
                Return_Row1 =DataFromCSV_2.Return_Row_Excel()
                ArraySelectedItem[0] = int(Count_Continue)
                DataFromCSV_DATA = DataFromCSV(*ArraySelectedItem)
                arr = DataFromCSV_DATA.GetContentDataFromExcel_Test()
                self.GetValueOfSelectedValue(arr)
                DataFromCSV_DATA.InputDataChangeToCSV_Excel(Return_Row1)
                self.InputNumberLeft.Text = str (int(Count_Continue - 1))
        except :
                print ("Check OK_Prevous")
    def Click_To_Start(self, sender, e):
            self.Close()
            DataToolTemplate = GetPath()
            SynChronizeValueToCSV_T()
            ArrDataExcell = GetArrDataExcell(DataToolTemplate)
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            arr = DataFromdem.GetContentDataFromExcel()
            DataFromdem = DataFromCSV(*arr)
            DataFromdem.Set_Count(1)
            DataFromdem.CreateElement()
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()