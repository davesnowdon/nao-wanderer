'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of actions the robot can take
'''

import sys

class Action(object):
    def __init__(self):
        super(Action, self).__init__()

class WalkStraight(Action):
    def __init__(self, distance):
        super(WalkStraight, self).__init__()
        self.distance = distance

class WalkAlways(WalkStraight):
    def __init__(self):
        super(WalkAlways, self).__init__(sys.maxint)

class WalkSideways(Action):
    def __init__(self):
        super(WalkStraight, self).__init__()

class Turn(Action):
    def __init__(self, direction):
        super(Turn, self).__init__()
        self.direction = direction

class Point(Action):
    def __init__(self):
        super(Point, self).__init__()

class Wave(Action):
    def __init__(self):
        super(Wave, self).__init__()

