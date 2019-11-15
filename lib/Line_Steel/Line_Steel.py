import clr
from Autodesk.Revit.DB import IntersectionResultArray,SetComparisonResult
from PySteelFraming.ConvertUnitRevit import ConvertFromInteralUnitToMM
class LineInterSection:
    def  __init__(self, line1, line2, line3, line4, path,Right_Member_All):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.line4 = line4
        self.path = path
        self.Right_Member_All = Right_Member_All
    def Getintersection (self):
        if path == self.Right_Member_All:
            self.line1 = self.line3
            self.line2 = self.line4
        results = clr.Reference[IntersectionResultArray]()
        result = self.line1.Intersect(self.line2, results)
        if result != SetComparisonResult.Overlap:
	        print('No Intesection, Review gird was choise')
        res = results.Item[0]
        return res.XYZPoint
    def GetDistanceRight (self,length):
        if path == self.Right_Member_All:
            Point1 = GetInterSectionTwoLine(self.line1,self.line2)
            Point2 = GetInterSectionTwoLine(self.line3,self.line4)
            Distance1 = Point2.X - Point1.X
            Distance1 = ConvertFromInteralUnitToMM(Distance1) - float(length)
        else:
            Distance1 = length
        return Distance1
    def GetInterSectionTwoLine (self):
        results = clr.Reference[IntersectionResultArray]()
        result = self.line1.Intersect(self.line2, results)
        if result != SetComparisonResult.Overlap:
	        print('No Intesection, Review gird was choise')
        res = results.Item[0]
        return res.XYZPoint