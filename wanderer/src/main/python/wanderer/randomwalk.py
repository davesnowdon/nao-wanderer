'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math
from random import Random

from util.general import *
from event import *
from action import *
from wanderer import Planner

class RandomWalk(Planner):

    def __init__(self, caller, proxies):
        super(RandomWalk, self).__init__(caller, proxies)
        self.rng = Random()

    def handleObstacleDetected(self, event, state):
        pass

    def handleStart(self, event, state):
        direction = self.rng.randint(0, 360)
        return [Turn(direction), WalkForwardsIndefinitely()]
    
    def handleBumpOccurred(self, event, state):
        moveIn = 'left' if event.side == 'right' else 'right'
        return [WalkForwards(-50), Turn(moveIn), WalkForwardsIndefinitely()]

    '''
    Take an event representing an obstruction and work out what
    direction to avoid.

    Returns two angles representing the min & max free orientations
    '''
def event_to_obstruction_direction(event):
    if is_obstruction(event):
        pass
    else:
        return (-math.pi, math.pi)

def is_obstruction(event):
    return not (event is None) and event.name() == class_to_name(ObstacleDetected)

