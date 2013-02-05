'''
Created on Jan 19, 2013

@author: dsnowdon
'''
import random
import math

from util.mathutil import to_radians

import robotstate
import event
import action

'''
Here we define the memory locations used to store state
'''
MEM_SECURITY_DISTANCE = "WandererSecurityDistance"
MEM_LOOK_FOR_FACES = "WandererLookForFaces"
MEM_HEADING = "WandererWalkHeading"
MEM_OBSTACLE_LOCATION = "WandererObstacleLocation"
MEM_WALK_PATH = "WandererWalkPath"
MEM_DETECTED_FACE_DIRECTION = "WandererFaceDirection"

'''
The various walking states
'''
STATE_WALK = "Walk"

def init_state(caller, memProxy, startPos):
    # getData & removeData throw errors if the value is not set, 
    # so just set to empty string
    memProxy.insertData(MEM_OBSTACLE_LOCATION, "")
    
    # set "security distance"
    memProxy.insertData(MEM_SECURITY_DISTANCE, "0.25")

    # set initial position (in list of positions)
    memProxy.insertData(MEM_WALK_PATH, [startPos])   

'''
Choose the next direction to head in
'''
def pick_direction(caller, memProxy, motionProxy, hOffset, bCtrBias):
    head = motionProxy.getAngles("Head", True)
    hHeadAngle = head[0]
    
    if bCtrBias and hHeadAngle > 0:
        hMax = hOffset * math.cos(hHeadAngle) 
        hMin = (-2 * hOffset) + hMax
    elif bCtrBias and hHeadAngle < 0:
        hMin = -hOffset * math.cos(hHeadAngle) 
        hMax = (2 * hOffset) + hMin
    else:
        hMin = -hOffset
        hMax = hOffset           
    
    # do we need to avoid an obstacle?
    obstruction = memProxy.getData(MEM_OBSTACLE_LOCATION)
    if obstruction == "left":
        caller.log("there is obstruction on right ")
        hMin = 0
    elif obstruction == "right":
        caller.log("there is obstruction on right ")
        hMax = 0
    elif obstruction == "centre":
        caller.log("there is obstruction in centre ")
    else:
        caller.log("no obstruction")
    
    caller.log("hMin = " + str(hMin) + ", hMax = " + str(hMax) + ", head angle = " + str(hHeadAngle) + ", head offset = " + str(hOffset))
        
    hDeg = random.uniform(hMin, hMax)
    return to_radians(hDeg)

def save_direction(caller, memProxy, hRad):
    memProxy.insertData(MEM_HEADING, hRad)

def obstacle_found(caller, memProxy, location):
    caller.log("obstacle found on "+str(location))
    memProxy.insertData(MEM_OBSTACLE_LOCATION, location)

def face_detected(caller, memProxy, currentPosition, faceDirection):
    caller.log("face detected")
    return STATE_WALK

def walking_started(caller, memProxy):
    caller.log("walking started")

def walking_stopped(caller, memProxy):
    caller.log("walking stopped")

def get_position(caller, motionProxy):
    # 1 = FRAME_WORLD
    return motionProxy.getPosition("Head", 1, True)

def save_waypoint(caller, memProxy, waypoint):
    path = memProxy.getData(MEM_WALK_PATH)
    path.append(waypoint)
    caller.log("Path = "+str(path))
    memProxy.insertData(MEM_WALK_PATH, path)

