'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math

#from util.general import *
#from wanderer.event import *
#from wanderer.action import *
from random import Random

class Wanderer(object):

    def __init__(self, caller, proxies):
        super(Wanderer, self).__init__()
        self.caller = caller
        self.proxies = proxies
        self.rng = Random()

    def handleEvent(self, event, state):
        plan = self.dispatch(event, state)
        proxies.memory.insertData("WandererActions", plan)

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
    Create a plan when we don't have an event to react to
    '''
    def handle_null_event(caller, proxies, state, event):
        # turn in a random direction and keep walking
        head = proxies.motion.getAngles("Head", True)
        headAngle = head[0]
        plan =[]
        plan.append(Turn(pick_direction(caller, headAngle, None, math.pi, True)))
        plan.append(WalkStraight(None))
        return plan

    def handle_obstacle(caller, proxies, state, event):
        pass

    def handle_face(caller, proxies, state, event):
        pass

    def handle_known_face(caller, proxies, state, event):
        pass

    def handle_known_object(caller, proxies, state, event):
        pass

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

