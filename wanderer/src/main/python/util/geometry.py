'''
Created on 13 Apr 2013

@author: dsnowdon
'''

import math

class Point(object):
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def subtract(self, p):
        self.x = self.x - p.x
        self.y = self.y - p.y
        
    def add(self, p):
        self.x = self.x + p.x
        self.y = self.y + p.y
    
    def clone(self):
        return Point(self.x, self.y)

'''
make a point from another point
'''
def fromPoint(p):
    return Point(p.x, p.y)

'''
returns p1+p2
'''
def pointSum(p1, p2):
    return Point(p1.x+p2.x, p1.y+p2.y)

'''
returns p1-p2
'''
def pointDifference(p1, p2):
    return Point(p1.x-p2.x, p1.y-p2.y)

def pointDistance(p1, p2):
    vec =pointDifference(p1, p2)
    return math.sqrt(vec.x*vec.x + vec.y*vec.y)
'''
Make  a vector from a starting point and a line of length radius rotated by angle
'''
def line_at_angle(startPoint, angle, radius):
    return Point(startPoint.x + radius*math.cos(angle), startPoint.y + radius*math.sin(angle))

'''
Represents a sector of a circle from a point (which would be the centre of the circle), a starting
and ending angle and a radius
'''
class CircleSector(object):
    def __init__(self, centre_, startAngle_, endAngle_, radius_):
        self.centre = centre_
        self.startAngle = startAngle_
        self.endAngle = endAngle_
        self.radius = radius_
        self.radiusSquared = self.radius * self.radius
        # pre-compute vectors that will be used for inside sector test
        self.sectorStart = line_at_angle(self.centre, self.startAngle, self.radius)
        self.sectorEnd = line_at_angle(self.centre, self.endAngle, self.radius)

    def is_inside(self, point):
        relPoint = pointDifference(point, self.centre)
        return not are_clockwise(self.sectorStart, relPoint) and \
            are_clockwise(self.sectorEnd, relPoint) and   \
            is_within_radius(relPoint, self.radiusSquared)


'''
Return true of point (1st param) is inside the circle sector described by the centre point (centre of
the circle that the sector is a segment of), two angles and a radius
'''
def is_inside_sector(point, centre, startAngle, endAngle, radius):
    radiusSquared = radius * radius
    relPoint = pointDifference(point, centre)
    sectorStart = line_at_angle(centre, startAngle, radius)
    sectorEnd = line_at_angle(centre, endAngle, radius)
    return not are_clockwise(sectorStart, relPoint) and \
        are_clockwise(sectorEnd, relPoint) and   \
        is_within_radius(relPoint, radiusSquared)

'''
Helper functions for is_inside_sector
'''
def are_clockwise(v1, v2):
    return -v1.x*v2.y + v1.y*v2.x > 0.0;

def is_within_radius(v, radiusSquared):
    return v.x*v.x + v.y*v.y <= radiusSquared;
