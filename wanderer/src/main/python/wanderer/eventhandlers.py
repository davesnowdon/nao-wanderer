'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math

from util.general import *
from event import *
from action import *
from random import Random

class Wanderer(object):

    def __init__(self, caller, proxies):
        super(Wanderer, self).__init__()
        self.caller = caller
        self.proxies = proxies
        self.rng = Random()

    def handleEvent(self, event, state):
        plan = self.dispatch(event, state)
        self.proxies.memory.insertData("WandererActions", plan)

    def dispatch(self, event, state):
        methodName = 'handle'+ event.name()
        method = getattr(self, methodName)
        return method(event, state)

    def handleObstacleDetected(self, event, state):
        pass

    def handleStart(self, event, state):
        direction = self.rng.randint(0, 360)
        return [Turn(direction), WalkAlways()]
    
    def handleBumpOccurred(self, event, state):
        moveIn = 'left' if event.side == 'right' else 'right'
        return [WalkStraight(-50), Turn(moveIn), WalkAlways()]

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

