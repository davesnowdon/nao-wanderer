'''
Created on 14 Apr 2013

@author: dns
'''
import unittest
from util.geometry import *

class TestCircleSector(unittest.TestCase):
    def test_inside_sector_by_angle(self):
        self.angle_with_inside_sector(Point(0,0), math.pi/4.0, math.pi/2.0, 5)
        
    def test_circle_sector_by_angle(self):
        sector = CircleSector(Point(0,0), math.pi/4.0, math.pi/2, 5)
        self.angle_with_circle_sector(sector, Point(0,0))

    def test_inside_sector_outside_range(self):
        one_degree = math.pi / 180.0
        centre = Point(0,0)
        startAngle = 0
        endAngle = math.pi/2
        radius = 5.0
        for x in range(360):
            angle = x * one_degree
            testPoint = line_at_angle(centre, angle, radius*2)
            isInside = is_inside_sector(testPoint, centre, startAngle, endAngle, radius)
            if isInside:
                self.fail(self.fail_msg(testPoint, centre, startAngle, endAngle, radius, "outside", 
                                    "is_inside_sector"))
        

    def test_circle_sector_outside_range(self):
        one_degree = math.pi / 180.0
        centre = Point(0,0)
        startAngle = 0
        endAngle = math.pi/2
        radius = 5.0
        sector = CircleSector(centre, startAngle, endAngle, radius)
        for x in range(360):
            angle = x * one_degree
            testPoint = line_at_angle(centre, angle, radius*2)
            isInside = sector.is_inside(testPoint)
            if isInside:
                self.fail(self.fail_msg(testPoint, centre, startAngle, endAngle, radius, "outside", 
                                    "CircleSector"))

    def angle_with_inside_sector(self, centre, startAngle, endAngle, radius):
        one_degree = math.pi / 180.0
        for x in range(360):
            angle = x * one_degree
            testPoint = line_at_angle(centre, angle, float(radius)/2.0)
            isInside = is_inside_sector(testPoint, centre, startAngle, endAngle, radius)
            if (angle >= startAngle) and (angle <= endAngle):
                # should be inside
                if not isInside:
                    self.fail(self.fail_msg(testPoint, centre, startAngle, endAngle, radius, 
                                            "inside", "is_inside_sector"))
            else:
                # should be outside
                if isInside:
                    self.fail(self.fail_msg(testPoint, centre, startAngle, endAngle, radius, 
                                            "outside", "is_inside_sector"))

    def angle_with_circle_sector(self, sector, testCentre):
        one_degree = math.pi / 180.0
        for x in range(360):
            angle = x * one_degree
            testPoint = line_at_angle(testCentre, angle, float(sector.radius)/2.0)
            isInside = sector.is_inside(testPoint)
            if (angle >= sector.startAngle) and (angle <= sector.endAngle):
                # should be inside
                if not isInside:
                    self.fail(self.fail_msg(testPoint, sector.centre, sector.startAngle, 
                                            sector.endAngle, sector.radius, "inside", "CircleSector"))
            else:
                # should be outside
                if isInside:
                    self.fail(self.fail_msg(testPoint, sector.centre, sector.startAngle, 
                                            sector.endAngle, sector.radius, "outside", "CircleSector"))

    def fail_msg(self, testPoint, centre, startAngle, endAngle, radius, insideOutside, methodUsed):
        return "FAIL: "+methodUsed+" point ("+str(testPoint.x)+", "+str(testPoint.y)+ \
               ") should be " + insideOutside + " sector ("+str(centre.x)+","+str(centre.y)+ \
               ") "+str(startAngle)+" - "+str(endAngle) + " radius = "+str(radius)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()