'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math

from util.general import *
from event import *
from action import *

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

def is_obstruction(event):
    return not (event is None) and event.name() == class_to_name(ObstacleDetected)

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