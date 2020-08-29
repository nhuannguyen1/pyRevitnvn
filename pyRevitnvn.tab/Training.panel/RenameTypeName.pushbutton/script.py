__doc__ = 'Training Revit at itivs '
__author__ = 'Nhuan'
__title__ = 'Rename Type Name'
from Autodesk.Revit.DB import Transaction 
from Autodesk.Revit.UI.Selection import ObjectType
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
from pyrevitnvn import retr_ele_from_pick,retr_eletype_from_ele

def get_parameter_value_by_name(element, parameterName):
    return element.LookupParameter(parameterName).AsString()

def set_parameter_by_name(element, parameterName, value):
   return element.LookupParameter(parameterName).Set(value)


#Retrieve element type from pick 1
ele = retr_ele_from_pick()
eleTypeId1 = retr_eletype_from_ele(ele)

# get Tw1 parameter of collumn 
Tw_Column_Rafter_WF = eleTypeId1.LookupParameter('Tw_Column_Rafter_WF').AsDouble()

# get T2 parameter of collumn 
T = eleTypeId1.LookupParameter('T').AsDouble()

#get W_T2 parameter of connection anchor bolt  
W_T2 = eleTypeId1.LookupParameter('W_T2').AsDouble()

FamilyNameType = str(Tw_Column_Rafter_WF)  +"x" + str(W_T2) + "x" + str(T) + "mm"

t = Transaction (doc,"Rename Type Name")
t.Start()
SymNew = eleTypeId1.Duplicate(FamilyNameType) 
ele.Symbol = SymNew
t.Commit()
