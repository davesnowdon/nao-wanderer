'''
Created on Jan 19, 2013

@author: dsnowdon
'''
import random
import math

from util.mathutil import to_radians
from util.general import *

import robotstate
from event import *
from action import *
from event_handlers import *

'''
Here we define the memory locations used to store state
'''
MEM_SECURITY_DISTANCE = "WandererSecurityDistance"
MEM_LOOK_FOR_FACES = "WandererLookForFaces"
MEM_HEADING = "WandererWalkHeading"
MEM_WALK_PATH = "WandererWalkPath"
MEM_DETECTED_FACE_DIRECTION = "WandererFaceDirection"
MEM_CURRENT_ACTIONS = "WandererActions"
MEM_COMPLETED_ACTIONS = "WandererActionsCompleted"
MEM_CURRENT_EVENT = "WandererEvent"


'''
Map to control functions used to react to events
'''
NULL_EVENT = "null"
EVENT_HANDLERS = {
                  NULL_EVENT : handle_null_event,
                  class_to_name(ObstacleDetected) : handle_obstacle,
                  class_to_name(FaceDetected) : handle_face,
                  class_to_name(FaceRecognised) : handle_known_face,
                  class_to_name(ObjectRecognised) : handle_known_object
                  }

CENTRE_BIAS = False
HEAD_HORIZONTAL_OFFSET = 0

def init_state(caller, proxies, startPos):
    # getData & removeData throw errors if the value is not set, 
    # so ensure all the memory locations we want to use are initialised
    proxies.memory.insertData(MEM_CURRENT_EVENT, None)
    
    # set "security distance"
    proxies.memory.insertData(MEM_SECURITY_DISTANCE, "0.25")

    # look for faces by default
    proxies.memory.insertData(MEM_LOOK_FOR_FACES, True)

    # set initial position (in list of positions)
    proxies.memory.insertData(MEM_WALK_PATH, [startPos])

    # current actions and completed actions
    proxies.memory.insertData(MEM_CURRENT_ACTIONS, [])
    proxies.memory.insertData(MEM_COMPLETED_ACTIONS, [])


'''
Base function for creating action plan
Generates plans (sequences of actions) in response to events. Can
change behaviour by modifying handlers map.
'''
def make_plan(caller, proxies, state, event):
    plan =[]
    if event is None:
        plan = EVENT_HANDLERS[NULL_EVENT](caller, proxies, state, event)
    else:
        plan = EVENT_HANDLERS[event.name()](caller, proxies, state, event)
    
    log_plan(caller, "New plan", plan)
    
    return plan

'''
Log a plan
'''
def log_plan(logger, msg, plan):
    logger.log(msg)
    for p in plan:
        logger.log(str(p))

def save_direction(caller, memProxy, hRad):
    memProxy.insertData(MEM_HEADING, hRad)

def get_position(caller, motionProxy):
    # 1 = FRAME_WORLD
    return motionProxy.getPosition("Head", 1, True)

def save_waypoint(caller, memProxy, waypoint):
    path = memProxy.getData(MEM_WALK_PATH)
    path.append(waypoint)
    caller.log("Path = "+str(path))
    memProxy.insertData(MEM_WALK_PATH, path)


