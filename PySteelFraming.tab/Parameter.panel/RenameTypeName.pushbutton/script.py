__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Rename Type Name'
from Autodesk.Revit.DB import*
from Autodesk.Revit.UI import*
from Autodesk.Revit.Attributes import*
from Autodesk.Revit.UI.Selection import ObjectType
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
ParameterValue = UnitUtils.ConvertToInternalUnits(444, DisplayUnitType.DUT_MILLIMETERS)
#paramdef = InternalDefinition()
    #Pick object 1 
pick1 = uidoc.Selection.PickObject(ObjectType.Element)
    #Pick object 2
pick2 = uidoc.Selection.PickObject(ObjectType.Element)
    #retrieve elenment 1
eleid1 = pick1.ElementId
ele1 = doc.GetElement(eleid1)
eleTypeId1 = doc.GetElement(ele1.GetTypeId())
    #retrieve elenment 2
eleid2 = pick2.ElementId
ele2 = doc.GetElement(eleid2)
eleTypeId2 = doc.GetElement(ele2.GetTypeId())
    # get Tw1 parameter of collumn 
Tw1_Parameter = eleTypeId1.LookupParameter('Tw1')
     # get T2 parameter of collumn 
T2_Parameter = eleTypeId1.LookupParameter('T2')
    #get W_T2 parameter of connection anchor bolt  
W_T2_Parameter = eleTypeId2.LookupParameter('W_T2')
    #get Tw_Column_Rafter_WF parameter of connection anchor bolt  
Tw_Column_Rafter_WF_Parmater = eleTypeId2.LookupParameter('Tw_Column_Rafter_WF')
    #get T parameter of connection anchor bolt
T_Parameter = eleTypeId2.LookupParameter('T')
    #Convert parameter to double 
Tw1_R = Tw1_Parameter.AsDouble()
T2_R = T2_Parameter.AsDouble()
W_T2_R = W_T2_Parameter.AsDouble()
Tw_Column_Rafter_WF_R = Tw_Column_Rafter_WF_Parmater.AsDouble()
T_R = T_Parameter.AsDouble()
    #conver unit display 
Tw1 = UnitUtils.Convert(Tw1_R,DisplayUnitType.DUT_DECIMAL_FEET,DisplayUnitType.DUT_MILLIMETERS)
T2 = UnitUtils.Convert(T2_R,DisplayUnitType.DUT_DECIMAL_FEET,DisplayUnitType.DUT_MILLIMETERS)
W_T2 = UnitUtils.Convert(W_T2_R,DisplayUnitType.DUT_DECIMAL_FEET,DisplayUnitType.DUT_MILLIMETERS)
Tw_Column_Rafter_WF = UnitUtils.Convert(Tw_Column_Rafter_WF_R,DisplayUnitType.DUT_DECIMAL_FEET,DisplayUnitType.DUT_MILLIMETERS)
T = UnitUtils.Convert(T_R,DisplayUnitType.DUT_DECIMAL_FEET,DisplayUnitType.DUT_MILLIMETERS)
    #get type name of family
eleTypeIdName = Element.Name.__get__(eleTypeId2)
familysymbols = eleTypeId2.Family
    #FamilyNameType = str(Tw_Column_Rafter_WF)  +"x" + str(W_T2) + "x" + str(T) + "mm"
FamilyNameType = str(Tw1)  +"x" + str(T2) + "x" + str(T) + "mm"
print (FamilyNameType)
Compare = 0
t = Transaction (doc,"Set parameter")
t.Start()
for familysymbol in familysymbols.GetFamilySymbolIds():
    ele_N = doc.GetElement(familysymbol)
        #eleT_NId = doc.GetElement(ele_N.GetTypeId())
        #FamilySymbolName = familysymbol.Name
    FamilySymbolName = Element.Name.__get__(ele_N)
        #print (FamilySymbolName)
    if (FamilySymbolName == FamilyNameType):
        symbol = doc.GetElement(familysymbol)
        ele2.Symbol = symbol
        Compare = 1
            #print (familysymbols)
if Compare==0:
        #EleSymbolActive = doc.GetElement(eleTypeId2)
    SymNew = eleTypeId2.Duplicate(FamilyNameType) 
    W_T2_Parameter_New = SymNew.LookupParameter('W_T2')
    #get Tw_Column_Rafter_WF parameter of connection anchor bolt  
    Tw_Column_Rafter_WF_Parmater_New = SymNew.LookupParameter('Tw_Column_Rafter_WF')
    #get T parameter of connection anchor bolt
    T_Parameter_New = SymNew.LookupParameter('T')
    W_T2_Parameter_New.Set(T2_R)
    Tw_Column_Rafter_WF_Parmater_New.Set(Tw1_R)
    ele2.Symbol = SymNew
t.Commit()