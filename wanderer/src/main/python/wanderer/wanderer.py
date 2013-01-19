'''
Created on Jan 19, 2013

@author: dsnowdon
'''
from naoqi import ALProxy

MEM_SECURITY_DISTANCE = "WandererSecurityDistance"
MEM_LOOK_FOR_FACES = "WandererLookForFaces"
MEM_OBSTACLE_LOCATION = "WandererObstacleLocation"
MEM_WALK_PATH = "WandererWalkPath"
MEM_DETECTED_FACE_DIRECTION = "WandererFaceDirection"

def init_state(memProxy):
    pass

def pick_direction(memProxy):
    pass

def obstacle_found(memProxy):
    pass

def face_detected(memProxy, currentPosition, faceDirection):
    pass

def walking_started(memProxy):
    pass

def walking_stopped(memProxy):
    pass

def save_waypoint(memProxy, waypoint):
    pass