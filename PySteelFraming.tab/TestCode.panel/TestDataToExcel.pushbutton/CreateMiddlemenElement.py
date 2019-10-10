from Autodesk.Revit.DB.Plane import CreateByThreePoints 
from Autodesk.Revit.DB import XYZ, ElementId,Transaction
from Autodesk.Revit.DB.ElementTransformUtils import MirrorElements
import ConvertAndCaculation
import rpw
from System.Collections.Generic import List
uidoc = rpw.revit.uidoc  # type: UIDocument
doc = rpw.revit.doc  # type: Document
def CreateElementByMirror (ArrElements,Getcondination,Length_From_Gird):
    #ArrElementId = [ArrElement.Id for ArrElement in ArrElements]
    t = Transaction (doc,"Create Mirror")
    t.Start()
    Length_From_Gird = ConvertAndCaculation.ConvertToInternalUnitsmm (Length_From_Gird)
    """
    Point1 = XYZ(Getcondination.X + Length_From_Gird,0,0)
    point2 = XYZ(Getcondination.X + Length_From_Gird,100,0)
    point3 = XYZ(Getcondination.X + Length_From_Gird,100,100)
    """
    Point1 = XYZ(Getcondination.X,0,0)
    point2 = XYZ(Getcondination.X,100,0)
    point3 = XYZ(Getcondination.X,100,100)
    #col1 = List[ElementId](ArrElementId)
    PlaneElement = CreateByThreePoints(Point1,point2,point3)
    MirrorElements(doc,ArrElements,PlaneElement,False)
    t.Commit()