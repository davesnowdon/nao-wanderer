'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of actions the robot can take
'''

class Action(object):
    def __init__(self):
        super(Action, self).__init__()
        

class WalkStraight(object):
    def __init__(self, distance):
        super(WalkStraight, self).__init__()
        self.distance = distance

class WalkSideways(object):
    def __init__(self):
        super(WalkStraight, self).__init__()

class Turn(object):
    def __init__(self, direction):
        super(Turn, self).__init__()
        self.direction = direction

class Point(object):
    def __init__(self):
        super(Point, self).__init__()

class Wave(object):
    def __init__(self):
        super(Wave, self).__init__()