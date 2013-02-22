'''
Created on Jan 19, 2013

@author: dsnowdon
'''

from util.general import to_json_string, from_json_string

import robotstate
from event import *
from action import *

'''
Here we define the memory locations used to store state
'''
MEM_SECURITY_DISTANCE = "WandererSecurityDistance"
MEM_LOOK_FOR_FACES = "WandererLookForFaces"
MEM_HEADING = "WandererWalkHeading"
MEM_WALK_PATH = "WandererWalkPath"
MEM_DETECTED_FACE_DIRECTION = "WandererFaceDirection"
MEM_PLANNED_ACTIONS = "WandererActionsPlanned"
MEM_CURRENT_ACTIONS = "WandererActionsInProgress"
MEM_COMPLETED_ACTIONS = "WandererActionsCompleted"
MEM_CURRENT_EVENT = "WandererEvent"


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
    proxies.memory.insertData(MEM_PLANNED_ACTIONS, "")
    proxies.memory.insertData(MEM_CURRENT_ACTIONS, "")
    proxies.memory.insertData(MEM_COMPLETED_ACTIONS, "")


'''
Base class for wanderer planning. 
Handles generating plans and reacting to events
'''
class Planner(object):
    def __init__(self, caller, proxies):
        super(Planner, self).__init__()
        self.caller = caller
        self.proxies = proxies

    def handleEvent(self, event, state):
        plan = self.dispatch(event, state)
        save_plan(self.proxies, plan)
        log_plan(self.caller, "New plan", plan)
        return plan

    def dispatch(self, event, state):
        methodName = 'handle'+ event.name()
        try:
            method = getattr(self, methodName)
            return method(event, state)
        except AttributeError:
            self.caller.log("Unimplemented event handler for: "+event.name())


'''
Base class for executing plans. Since we may need to trigger choreographe
boxes we delegate actually performing a single action to an actionExecutor
which in most cases will be the choreographe box that called us.

The actionExecutor must implement do_action(action) and all_done()
'''
class PlanExecutor(object):
    def __init__(self, caller, proxies, actionExecutor):
        super(PlanExecutor, self).__init__()
        self.caller = caller
        self.proxies = proxies
        self.actionExecutor = actionExecutor

    def perform_next_action(self):
        self.caller.log("perform next action")
        # save completed action to history if there is one
        completedAction = get_current_action(self.proxies)
        self.caller.log("Completed action = "+repr(completedAction))
        if not completedAction is None:
            if not isinstance(completedAction, NullAction):
                push_completed_action(self.proxies, completedAction)
                # if we have moved, then save current location
                if isinstance(completedAction, Move):
                    self._have_moved_wrapper()
        
        self.caller.log("set current action to NullAction")
        # ensure that current action is cleared until we have another one        
        set_current_action(self.proxies, NullAction())
        
        self.caller.log("pop from plan")
        # pop first action from plan
        action = pop_planned_action(self.proxies)
        if action is None:
            self.caller.log("No next action")
            self.actionExecutor.all_done()
        else:
            self.caller.log("Next action = "+repr(action))
            set_current_action(self.proxies, action)
            self.actionExecutor.do_action(action)
        self.caller.log("perform_next_action done")

    # get current and previous positions and call have_moved
    # it's not intended that this method be overridden
    def _have_moved_wrapper(self):
        self.caller.log("Have moved")
        pos = get_position(self.caller, self.proxies)
        lastPos = get_last_position(self.caller, self.proxies)
        self.have_moved(lastPos, pos)
        save_waypoint(self.caller, self.proxies, pos)

    # hook for base classes to implement additional functionality
    # after robot has moved
    def have_moved(self, previousPos, currentPos):
        pass

    def save_position(self):
        pos = get_position(self.caller, self.proxies)
        save_waypoint(self.caller, self.proxies, pos)

def load_event(proxies):
    return from_json_string(proxies.memory.getData(MEM_CURRENT_EVENT))

def save_event(proxies, event):
    proxies.memory.insertData(MEM_CURRENT_EVENT, to_json_string(event))

def load_plan(proxies):
    return from_json_string(proxies.memory.getData(MEM_PLANNED_ACTIONS))
    
def save_plan(proxies, plan):
    proxies.memory.insertData(MEM_PLANNED_ACTIONS, to_json_string(plan))

def load_completed_actions(proxies):
    return from_json_string(proxies.memory.getData(MEM_COMPLETED_ACTIONS))
    
def save_completed_actions(proxies, actions):
    proxies.memory.insertData(MEM_COMPLETED_ACTIONS, to_json_string(actions))

def pop_planned_action(proxies):
    plan = load_plan(proxies)
    action = None
    if not plan is None:
        if len(plan) > 0:
            action = plan[0]
            plan = plan[1:]
        else:
            plan = []
        save_plan(proxies, plan)
    return action

def get_current_action(proxies):
    return from_json_string(proxies.memory.getData(MEM_CURRENT_ACTIONS))

def set_current_action(proxies, action):
    proxies.memory.insertData(MEM_CURRENT_ACTIONS, to_json_string(action))

def push_completed_action(proxies, action):
    actions = load_completed_actions(proxies)
    if actions is None:
        actions = []
    actions.append(action)
    save_completed_actions(proxies, actions)

def log_plan(logger, msg, plan):
    logger.log(msg)
    for p in plan:
        logger.log(str(p))

def save_direction(caller, memProxy, hRad):
    memProxy.insertData(MEM_HEADING, hRad)

'''
Get the last position the robot was at by looking at the path
'''
def get_last_position(caller, proxies):
    path = proxies.memory.getData(MEM_WALK_PATH)
    pos = None
    if not path is None:
        try:
            pos = path[-1]
        except IndexError:
            pass
    return pos

'''
Get the current position of the robot
'''
def get_position(caller, proxies):
    # 1 = FRAME_WORLD
    return proxies.motion.getPosition("Head", 1, True)

def save_waypoint(caller, proxies, waypoint):
    path = proxies.memory.getData(MEM_WALK_PATH)
    if path is None:
        path = []
    path.append(waypoint)
    caller.log("Path = "+str(path))
    proxies.memory.insertData(MEM_WALK_PATH, path)

