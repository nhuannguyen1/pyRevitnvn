__doc__ = 'Training Revit At Itivs '
__author__ = 'Nguyen Nhuan'
__title__ = 'Test Code'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,\
BuiltInCategory,FamilySymbol,Element,Family,Level,Grid
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Creation.Document import NewFamilyInstance
from pyrevit import script, forms
import os.path 
import clr
import CreatePrimaryFraming
import rpw
from GlobalParameter import setparameterfromvalue,DataFromCSV,\
    CheckSelectedValueForFamily,ArrFistForDefautValue_FC,CountNumberOfRow,\
        CountNumberOfColumn,GetPath_Left_Member_All,GetPath_Right_Member_All,writeRowTitle
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
from pyrevit.forms import WPFWindow
from DirectoryPath import Path_Config_Setting
from Csv_Connect_Data import DataCSV,ReturnArrContainSelectedAndText,GetDataToPrimaryFile
from CheckAndChoice import GetFixLevel

from DirectoryPath import ReturnDataAllRowByIndex_path

ReturnDataAllRowByIndex_path_Count = ReturnDataAllRowByIndex_path(Path_Config_Setting,2)

def GetArrDataExcell(DataToolTemplate):
    DataCSV1 = DataCSV(DataToolTemplate)
    DataCSV1.writeRowTitle(Path_Config_Setting)
    ArrDataExcell = ArrFistForDefautValue_FC(DataToolTemplate)
    return ArrDataExcell
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
        self.Select_Member.DataContext = GetFixLevel(4)
        self.Select_Level.DataContext = GetFixLevel(5)
        self.Choose_Purlin.DataContext = [vt for vt in FilteredElementCollector(doc).OfClass(Family) if vt.FamilyCategory.Name == "Structural Framing"]
        # Create Level
    def SelectLevelChoose_CH(self,sender,e):
        self.LevelChoose_CH = sender.SelectedItem
        if  self.LevelChoose_CH != None:
            self.Top_Level.SelectedValue = self.LevelChoose_CH.Name  
            self.Level_Rater_Type_Left.SelectedValue = self.LevelChoose_CH.Name  
    def Ok_Member_Select(self, sender, e):
        #try:
            self.InputNumberLeft.Text = str (1)
            DataToolTemplate = self.ReturnPath()
            ArrDataExcell = GetArrDataExcell(DataToolTemplate)
            count_dem = CountNumberOfRow(DataToolTemplate) - 1
            self.SetValueFromContentData(ArrDataExcell,count_dem)
        #except:
            #print ("no Object selected")
    def SetValueFromContentData (self,ArrDataExcell,count_dem):
        DataToolTemplate = self.ReturnPath()
        if count_dem != 0:
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            DataFromdem.SetPath(DataToolTemplate)
            GetDataFirst = DataFromdem.GetContentDataFromExcel(DataToolTemplate,0)
            self.GetValueOfSelectedValue(GetDataFirst,"P")
        else:
            GetDataFirst = ArrDataExcell
            self.GetValueOfSelectedValue(GetDataFirst,"P")
    def ReturnPath(self):
        GetFixLevellr4 =GetFixLevel(4)
        Select_Membered = self.Select_Member.SelectedItem
        try:
            if Select_Membered == GetFixLevellr4[0]:
                DataToolTemplate = GetPath_Left_Member_All()
                DataToolTemplateOther = GetPath_Right_Member_All()
            elif Select_Membered == GetFixLevellr4[1]:
                DataToolTemplate = GetPath_Right_Member_All() 
                DataToolTemplateOther = GetPath_Left_Member_All()
            else:
                DataToolTemplate = ""
            return DataToolTemplate
        except:
            print ("Check again ReturnPath")
    
    def ReturnPath_Rev(self):
            GetFixLevellr4 =GetFixLevel(4)
            Select_Membered = self.Select_Member.SelectedItem
            try:
                if Select_Membered == GetFixLevellr4[0]:
                    DataToolTemplate = GetPath_Left_Member_All()
                    DataToolTemplateOther = GetPath_Right_Member_All()
                elif Select_Membered == GetFixLevellr4[1]:
                    DataToolTemplate = GetPath_Right_Member_All() 
                    DataToolTemplateOther = GetPath_Left_Member_All()
                else:
                    DataToolTemplate = ""
                return DataToolTemplateOther
            except:
                print ("Check again ReturnPath_Rev")
    def GetValueOfSelectedValue(self,GetDataFirst,P):
        DATAS = DataCSV(Path_Config_Setting)
        strIndex = DATAS.ReturnDataAllRowByIndexpath(Path_Config_Setting,0)
        ArrContainSelectedAndText = ReturnArrContainSelectedAndText(Path_Config_Setting,7,8,9,"SelectedValue","Text")
        #print (GetDataFirst)
        for i in range(1,len(ArrContainSelectedAndText)):
            if P=="P":
                if  i in [4,10]:
                    continue
            else:
                if str(i) in strIndex:
                    continue
            arrTotal = ArrContainSelectedAndText[i] + " = "+ "CheckSelectedValueForFamily(GetDataFirst[{}])".format(i)
            exec(arrTotal)
    def Reset_Data(self, sender, e):
        try:
            DataToolTemplate = self.ReturnPath()
            ArrDataExcell = GetArrDataExcell(DataToolTemplate)
            DataFromdem = DataFromCSV(*ArrDataExcell)
            DataFromdem.Set_Count(1)
            DataFromdem.SetPath(DataToolTemplate)
            DataFromdem.DeleteRowToReset(DataToolTemplate)
            self.InputNumberLeft.Text = str (1)
        except:
            print ("Recheck Reset_Data function")
    def ChangeSelectType (self,sender,e):
        GetFixLevellr =GetFixLevel(5)
        self.LevelSelected = sender.SelectedItem
        if (self.LevelSelected ==GetFixLevellr[0]):
            self.Clear_Height.DataContext = self.levels
            self.Eave_Height.DataContext = None
            self.Peak_Height.DataContext = None
        elif (self.LevelSelected == GetFixLevellr[1]):
            self.Clear_Height.DataContext  = self.levels
            self.Peak_Height.DataContext = self.levels
            self.Eave_Height.DataContext = None
        elif (self.LevelSelected == GetFixLevellr[2]):
            self.Eave_Height.DataContext  = self.levels
            self.Clear_Height.DataContext = None
            self.Peak_Height.DataContext = None
        elif (self.LevelSelected == GetFixLevellr[3]):
            self.Peak_Height.DataContext = self.levels
            self.Eave_Height.DataContext = self.levels
            self.Clear_Height.DataContext = None
        else:
            print ("check ChangeSelectType")
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
    def ChangedPurlinName(self, sender, e):
        try:
            self.ChangedPurlin = sender.SelectedItem
            self.Choose_Type_Purlin.DataContext =[vt for vt in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).OfClass(FamilySymbol) if vt.FamilyName ==  self.ChangedPurlin.Name]
        except:
            pass   
    def ArraySelectedItemfs(self,Count_Continue):
        ArrContainSelectedAndText = ReturnArrContainSelectedAndText(Path_Config_Setting,7,8,9,"SelectedItem","Text")
        ArraySelectedItem_Text = [eval(vt) for vt in ArrContainSelectedAndText]
        return ArraySelectedItem_Text
    def Ok_Next(self, sender, e):
        try:
            Count_Continue = int(self.InputNumberLeft.Text)
            DataToolTemplate = self.ReturnPath()
            count_dem = CountNumberOfRow(DataToolTemplate) - 1
            ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
            DataFromCSV_1 = DataFromCSV(*ArraySelectedItem)
            DataFromCSV_1.SetPath(DataToolTemplate)
            if (Count_Continue > (count_dem) and Count_Continue != 1):
                #a = Count_Continue
                DataFromCSV_1.Set_Count(Count_Continue)
                DataFromCSV_1.writefileExcel(Count_Continue,DataToolTemplate)
            elif (Count_Continue == 1 and count_dem == 1):
                Return_Row1 =DataFromCSV_1.Return_Row()
                ArraySelectedItem [0] = Count_Continue 
                DataFromCSV_1 = DataFromCSV(*ArraySelectedItem)
                DataFromCSV_1.SetPath(DataToolTemplate)
                arr = DataFromCSV_1.GetContentDataFromExcel(DataToolTemplate,0)
                self.GetValueOfSelectedValue(arr,"")
                DataFromCSV_1.InputDataChangeToCSV_Excel(Return_Row1,DataToolTemplate)
            elif (Count_Continue == count_dem):
                DataFromCSV_1.Set_Count(Count_Continue)
                Return_Row1 =DataFromCSV_1.Return_Row()
                arr = DataFromCSV_1.GetContentDataFromExcel(DataToolTemplate,0)
                self.GetValueOfSelectedValue(arr,"")
                DataFromCSV_1.InputDataChangeToCSV_Excel(Return_Row1,DataToolTemplate)
            else:
                DataFromCSV_1.Set_Count(Count_Continue)
                Return_Row1 =DataFromCSV_1.Return_Row()
                arr = DataFromCSV_1.GetContentDataFromExcel(DataToolTemplate,1)
                self.GetValueOfSelectedValue(arr,"")
                DataFromCSV_1.InputDataChangeToCSV_Excel(Return_Row1,DataToolTemplate)
            DataCSV1 = DataCSV(DataToolTemplate)
            DataCSV1.SynChronizeValueToCSV1(Path_Config_Setting,Count_Continue)
            self.InputNumberLeft.Text = str (int(Count_Continue + 1))
            GetDataToPrimaryFile(DataToolTemplate,self.ReturnPath_Rev(),Path_Config_Setting,1)
        except AttributeError:
            print ("Check Ok_Next And Path Selected Yes Or No")
    def Ok_Prevous(self, sender, e):
        try:
            DataToolTemplate = self.ReturnPath()
            count_dem = CountNumberOfRow(DataToolTemplate)
            Count_Continue = int(self.InputNumberLeft.Text)
            if count_dem == Count_Continue:
                ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
                DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
                DataFromCSV_2.SetPath(DataToolTemplate)
                Return_Row1 =DataFromCSV_2.Return_Row()
                DataCSV1 = DataCSV(DataToolTemplate)
                DataCSV1.DataForLastRowIndex(Count_Continue,Return_Row1)
                self.InputNumberLeft.Text = str (int(Count_Continue) - 1)
                DataFromCSV_DATA = DataFromCSV(*ArraySelectedItem)
                DataFromCSV_DATA.SetPath(DataToolTemplate)
                arr = DataFromCSV_DATA.GetContentDataFromExcel(DataToolTemplate,-1)
                self.GetValueOfSelectedValue(arr,"")
            else:
                ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
                DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
                Return_Row1 =DataFromCSV_2.Return_Row()
                ArraySelectedItem[0] = int(Count_Continue)
                DataFromCSV_DATA = DataFromCSV(*ArraySelectedItem)
                DataFromCSV_DATA.SetPath(DataToolTemplate)
                arr = DataFromCSV_DATA.GetContentDataFromExcel(DataToolTemplate,-1)
                self.GetValueOfSelectedValue(arr,"")
                DataFromCSV_DATA.InputDataChangeToCSV_Excel(Return_Row1,DataToolTemplate)
                self.InputNumberLeft.Text = str (int(Count_Continue - 1))
            DataCSV1 = DataCSV(DataToolTemplate)
            DataCSV1.SynChronizeValueToCSV1(Path_Config_Setting,Count_Continue)
        except AttributeError :
                print ("Check OK_Prevous")
    def Click_To_Start(self, sender, e):
        #try:
            Count_Continue = int(self.InputNumberLeft.Text)
            DataToolTemplate = self.ReturnPath()
            ArraySelectedItem = self.ArraySelectedItemfs(Count_Continue)
            DataFromCSV_2 = DataFromCSV(*ArraySelectedItem)
            DataFromCSV_2.SetPath(DataToolTemplate)
            Return_Row1 = DataFromCSV_2.Return_Row()
            DataCSV1 = DataCSV(DataToolTemplate)
            DataCSV1.DataForLastRowIndex(Count_Continue,Return_Row1)
            DataCSV1.SysWhenStart(Return_Row1,Count_Continue,Path_Config_Setting)
            GetDataToPrimaryFile(DataToolTemplate,self.ReturnPath_Rev(),Path_Config_Setting,1)
            self.Close()
            CreatePrimaryFraming.PrimaryFraming()
        #except:
            #print ("Check Selectd Level")
WPF_PYTHON = WPF_PYTHON('WPF_PYTHON.xaml').ShowDialog()