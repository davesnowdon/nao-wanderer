'''
Created on 18 Apr 2013

@author: davesnowdon
'''
import math
import unittest

from wanderer.robotstate import Sensors
from wanderer.event import ObstacleDetected
from wanderer.randomwalk import event_to_obstruction_direction

class Test(unittest.TestCase):
    
    def test_obstacle_dead_ahead(self):
        sensors = Sensors({'LeftBumper' : False, 
                           'RightBumper' : False, 
                           'LeftSonar' : 0.3, 
                           'RightSonar' : 0.3})
        ev = ObstacleDetected('LeftSonar', sensors, [0.0,0.0,0.0,0.0,0.0,0.0])
        (tmin, tmax) = event_to_obstruction_direction(ev)
        print "tmin = "+str(tmin)+", tmax = "+str(tmax)
        self.assertGreaterEqual(tmin, math.pi/2, "Must turn at least 90 degrees right")
        self.assertLessEqual(tmax, math.pi*1.5, "Must turn at least 90 degrees left")
    
    def test_obstacle_on_right(self):
        sensors = Sensors({'LeftBumper' : False, 
                           'RightBumper' : False, 
                           'LeftSonar' : 2.5, 
                           'RightSonar' : 0.3})
        ev = ObstacleDetected('RightSonar', sensors, [0.0,0.0,0.0,0.0,0.0,0.0])
        (tmin, tmax) = event_to_obstruction_direction(ev)
        print "tmin = "+str(tmin)+", tmax = "+str(tmax)
        self.assertGreater(tmin, 0.0, "Must turn to left")
    
    def test_obstacle_on_left(self):
        sensors = Sensors({'LeftBumper' : False, 
                           'RightBumper' : False, 
                           'LeftSonar' : 0.3, 
                           'RightSonar' : 2.5})
        ev = ObstacleDetected('LeftSonar', sensors, [0.0,0.0,0.0,0.0,0.0,0.0])
        (tmin, tmax) = event_to_obstruction_direction(ev)
        print "tmin = "+str(tmin)+", tmax = "+str(tmax)
        self.assertLess(tmin, 0.0, "Must turn to right")
    
    def test_obstacle_closer_on_right(self):
        sensors = Sensors({'LeftBumper' : False, 
                           'RightBumper' : False, 
                           'LeftSonar' : 0.5, 
                           'RightSonar' : 0.3})
        ev = ObstacleDetected('RightSonar', sensors, [0.0,0.0,0.0,0.0,0.0,0.0])
        (tmin, tmax) = event_to_obstruction_direction(ev)
        print "tmin = "+str(tmin)+", tmax = "+str(tmax)
        self.assertGreater(tmin, 0.0, "Must turn to left")
    
    def test_obstacle_closer_on_left(self):
        sensors = Sensors({'LeftBumper' : False, 
                           'RightBumper' : False, 
                           'LeftSonar' : 0.3, 
                           'RightSonar' : 0.5})
        ev = ObstacleDetected('LeftSonar', sensors, [0.0,0.0,0.0,0.0,0.0,0.0])
        (tmin, tmax) = event_to_obstruction_direction(ev)
        print "tmin = "+str(tmin)+", tmax = "+str(tmax)
        self.assertLess(tmin, 0.0, "Must turn to right")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()