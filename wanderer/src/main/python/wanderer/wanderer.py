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

def init_state(env, startPos):
    # getData & removeData throw errors if the value is not set, 
    # so ensure all the memory locations we want to use are initialised
    env.memory.insertData(MEM_CURRENT_EVENT, None)
    
    # set "security distance"
    env.memory.insertData(MEM_SECURITY_DISTANCE, "0.25")

    # look for faces by default
    env.memory.insertData(MEM_LOOK_FOR_FACES, True)

    # set initial position (in list of positions)
    env.memory.insertData(MEM_WALK_PATH, [startPos])

    # current actions and completed actions
    env.memory.insertData(MEM_PLANNED_ACTIONS, "")
    env.memory.insertData(MEM_CURRENT_ACTIONS, "")
    env.memory.insertData(MEM_COMPLETED_ACTIONS, "")


'''
Base class for wanderer planning. 
Handles generating plans and reacting to events
'''
class Planner(object):
    def __init__(self, env_):
        super(Planner, self).__init__()
        self.env = env_

    def handleEvent(self, event, state):
        plan = self.dispatch(event, state)
        save_plan(self.env, plan)
        log_plan(self.env, "New plan", plan)
        return plan

    def dispatch(self, event, state):
        methodName = 'handle'+ event.name()
        try:
            method = getattr(self, methodName)
            return method(event, state)
        except AttributeError:
            self.env.log("Unimplemented event handler for: "+event.name())


'''
Base class for executing plans. Since we may need to trigger choreographe
boxes we delegate actually performing a single action to an actionExecutor
which in most cases will be the choreographe box that called us.

The actionExecutor must implement do_action(action) and all_done()
'''
class PlanExecutor(object):
    def __init__(self, env, actionExecutor):
        super(PlanExecutor, self).__init__()
        self.env = env
        self.actionExecutor = actionExecutor

    def perform_next_action(self):
        self.env.log("perform next action")
        # save completed action to history if there is one
        completedAction = get_current_action(self.env)
        self.env.log("Completed action = "+repr(completedAction))
        if not completedAction is None:
            if not isinstance(completedAction, NullAction):
                push_completed_action(self.env, completedAction)
                # if we have moved, then save current location
                if isinstance(completedAction, Move):
                    self._have_moved_wrapper()
        
        self.env.log("set current action to NullAction")
        # ensure that current action is cleared until we have another one        
        set_current_action(self.env, NullAction())
        
        self.env.log("pop from plan")
        # pop first action from plan
        action = pop_planned_action(self.env)
        if action is None:
            self.env.log("No next action")
            self.actionExecutor.all_done()
        else:
            self.env.log("Next action = "+repr(action))
            set_current_action(self.env, action)
            self.actionExecutor.do_action(action)
        self.env.log("perform_next_action done")

    # get current and previous positions and call have_moved
    # it's not intended that this method be overridden
    def _have_moved_wrapper(self):
        self.env.log("Have moved")
        pos = get_position(self.env)
        lastPos = get_last_position(self.env)
        self.have_moved(lastPos, pos)
        save_waypoint(self.env, pos)

    # hook for base classes to implement additional functionality
    # after robot has moved
    def have_moved(self, previousPos, currentPos):
        pass

    def save_position(self):
        pos = get_position(self.env)
        save_waypoint(self.env, pos)

def load_event(env):
    return from_json_string(env.memory.getData(MEM_CURRENT_EVENT))

def save_event(env, event):
    env.memory.insertData(MEM_CURRENT_EVENT, to_json_string(event))

def load_plan(env):
    return from_json_string(env.memory.getData(MEM_PLANNED_ACTIONS))
    
def save_plan(env, plan):
    env.memory.insertData(MEM_PLANNED_ACTIONS, to_json_string(plan))

def load_completed_actions(env):
    return from_json_string(env.memory.getData(MEM_COMPLETED_ACTIONS))
    
def save_completed_actions(env, actions):
    env.memory.insertData(MEM_COMPLETED_ACTIONS, to_json_string(actions))

def pop_planned_action(env):
    plan = load_plan(env)
    action = None
    if not plan is None:
        if len(plan) > 0:
            action = plan[0]
            plan = plan[1:]
        else:
            plan = []
        save_plan(env, plan)
    return action

def get_current_action(env):
    return from_json_string(env.memory.getData(MEM_CURRENT_ACTIONS))

def set_current_action(env, action):
    env.memory.insertData(MEM_CURRENT_ACTIONS, to_json_string(action))

def push_completed_action(env, action):
    actions = load_completed_actions(env)
    if actions is None:
        actions = []
    actions.append(action)
    save_completed_actions(env, actions)

def log_plan(env, msg, plan):
    env.log(msg)
    for p in plan:
        env.log(str(p))

def save_direction(env, hRad):
    env.memory.insertData(MEM_HEADING, hRad)

'''
Get the last position the robot was at by looking at the path
'''
def get_last_position(env):
    path = env.memory.getData(MEM_WALK_PATH)
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
def get_position(env):
    # 1 = FRAME_WORLD
    return env.motion.getPosition("Head", 1, True)

def save_waypoint(env, waypoint):
    path = env.memory.getData(MEM_WALK_PATH)
    if path is None:
        path = []
    path.append(waypoint)
    env.log("Path = "+str(path))
    env.memory.insertData(MEM_WALK_PATH, path)

