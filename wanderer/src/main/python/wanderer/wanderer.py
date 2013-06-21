'''
Created on Jan 19, 2013

@author: dsnowdon
'''

import os
import tempfile
import datetime
import json
import logging

from naoutil.jsonobj import to_json_string, from_json_string
from naoutil.general import find_class

import robotstate
from event import *
from action import *
from naoutil.naoenv import make_environment

'''
Here we define the memory locations used to store state
'''
MEM_SECURITY_DISTANCE = "WandererSecurityDistance"
MEM_HEADING = "WandererWalkHeading"
MEM_WALK_PATH = "WandererWalkPath"
MEM_DETECTED_FACE_DIRECTION = "WandererFaceDirection"
MEM_PLANNED_ACTIONS = "WandererActionsPlanned"
MEM_CURRENT_ACTIONS = "WandererActionsInProgress"
MEM_COMPLETED_ACTIONS = "WandererActionsCompleted"
MEM_CURRENT_EVENT = "WandererEvent"
MEM_MAP = "WandererMap"
MEM_LOCATION = "WandererLocation"

EVENT_LOOK_FOR_PEOPLE = "WandererEventLookForPeople"

DEFAULT_CONFIG_FILE = "wanderer"
PROPERTY_PLANNER_CLASS = "plannerClass"
DEFAULT_PLANNER_CLASS = "wanderer.randomwalk.RandomWalk"
PROPERTY_EXECUTOR_CLASS = "executorClass"
DEFAULT_EXECUTOR_CLASS = "wanderer.wanderer.PlanExecutor"
PROPERTY_MAPPER_CLASS = "mapperClass"
DEFAULT_MAPPER_CLASS = "wanderer.wanderer.NullMapper"
PROPERTY_UPDATER_CLASSES = "updaterClasses"
PROPERTY_HTTP_PORT = "httpPort"
DEFAULT_HTTP_PORT = 8080
PROPERTY_DATA_COLLECTOR_HOST = "dataCollectorHost"
PROPERTY_DATA_COLLECTOR_PORT = "dataCollectorPort"
PROPERTY_LOOK_FOR_PEOPLE = "lookForPeople"
STATIC_WEB_DIR = "web"

CENTRE_BIAS = False
HEAD_HORIZONTAL_OFFSET = 0
WANDERER_NAME = "wanderer"

# START GLOBALS
# We put instances of planners, executors and mappers here so we don't need to continually create
# new instances
planner_instance = None
executor_instance = None
mapper_instance = None
updater_instances = None
# END GLOBALS 

wanderer_logger = logging.getLogger("wanderer.wanderer")

def init_state(env, startPos):
    # declare events
    env.memory.declareEvent(EVENT_LOOK_FOR_PEOPLE);
    
    # getData & removeData throw errors if the value is not set, 
    # so ensure all the memory locations we want to use are initialised
    env.memory.insertData(MEM_CURRENT_EVENT, None)
    
    # set "security distance"
    env.memory.insertData(MEM_SECURITY_DISTANCE, "0.25")

    # should we look for people as we go?
    lookForPeople = env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_LOOK_FOR_PEOPLE)
    if lookForPeople:
        env.memory.raiseEvent(EVENT_LOOK_FOR_PEOPLE, True)
        env.log("Looking for people")
    else:
        env.memory.raiseEvent(EVENT_LOOK_FOR_PEOPLE, False)
        env.log("Not looking for people")

    # set initial position (in list of positions)
    env.memory.insertData(MEM_WALK_PATH, [startPos])

    # current actions and completed actions
    env.memory.insertData(MEM_PLANNED_ACTIONS, "")
    env.memory.insertData(MEM_CURRENT_ACTIONS, "")
    env.memory.insertData(MEM_COMPLETED_ACTIONS, "")

def shutdown(env):
    planner = get_planner_instance(env)
    planner.shutdown()

    executor = get_executor_instance(env, None)
    executor.shutdown()

    mapper = get_mapper_instance(env)
    mapper.shutdown()

    updater_instances = get_updaters(env)
    for updater in updater_instances:
        updater.shutdown()

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

    # return true if this event should cause the current plan to be executed and
    # a new plan created to react to it
    def does_event_interrupt_plan(self, event, state):
        return True

    def dispatch(self, event, state):
        methodName = 'handle'+ event.name()
        try:
            method = getattr(self, methodName)
            return method(event, state)
        except AttributeError:
            self.env.log("Unimplemented event handler for: {}".format(event.name()))

    def shutdown(self):
        pass


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
        self.env.log("Completed action = {}".format(repr(completedAction)))
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
            self.env.log("Next action = {}".format(repr(action)))
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

    def shutdown(self):
        pass
    
'''
Abstract mapping class
'''
class AbstractMapper(object):
    def __init__(self, env):
        super(AbstractMapper, self).__init__()
        self.env = env
    
    # update map based on new sensor data
    def update(self, position, sensors):
        pass
    
    # return the current map
    def get_map(self):
        return None

    def shutdown(self):
        pass

'''
Null mapper - does nothing, just a place holder for when no mapping is actually required
'''
class NullMapper(AbstractMapper):
    def __init__(self, env):
        super(NullMapper, self).__init__(env)


'''
Mapper that does no actual mapping, but logs all data to file for future analysis
'''
class FileLoggingMapper(AbstractMapper):
    def __init__(self, env, save_data=True):
        super(FileLoggingMapper, self).__init__(env)
        self.save_data = save_data
        if self.save_data:
            self.open_data_file()

    # save the data to file
    def update(self, position, sensors):
        if self.save_data:
            self.save_update_data(position, sensors)
    
    def open_data_file(self):
        self.logFilename = tempfile.mktemp()
        self.env.log("Saving sensor data to {}".format(self.logFilename))
        self.first_write = True
        try:
            self.logFile = open(self.logFilename, 'r+')
        except IOError:
            self.env.log("Failed to open file: {}".format(self.logFilename))
            self.logFile = None
    
    def save_update_data(self, position, sensors):
        if self.logFile:
            data = { 'timestamp' : self.timestamp(),
                     'position' : position,
                     'leftSonar' : sensors.get_sensor('LeftSonar'),
                     'rightSonar' : sensors.get_sensor('RightSonar') }
            jstr = json.dumps(data)
            #self.env.log("Mapper.update: "+jstr)

            if not self.first_write:
                self.logFile.write(",\n")
            self.logFile.write(jstr)
            self.first_write = False
            self.logFile.flush()

    def timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    
    # TODO should really block write access while doing this
    def write_sensor_data_to_file(self, fp, buffer_size=1024):
        if self.logFile:
            self.logFile.seek(0)
            fp.write('[\n')
            while 1:
                copy_buffer = self.logFile.read(buffer_size)
                if copy_buffer:
                    fp.write(copy_buffer)
                else:
                    break
            fp.write(' ]\n')
            self.logFile.seek(0, 2)

    def shutdown(self):
        if self.logFile:
            self.logFile.close()


'''
Get the instance of the planner, creating an instance of the configured class if we don't already
have a planner instance
'''
def get_planner_instance(env):
    global planner_instance
    if not planner_instance:
        fqcn = env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_PLANNER_CLASS, DEFAULT_PLANNER_CLASS)
        env.log("Creating a new planner instance of {}".format(fqcn))
        klass = find_class(fqcn)
        planner_instance = klass(env)
    return planner_instance

'''
Get the instance of the plan executor, creating an instance of the class specified in the configuration
file if necessary.
'''
def get_executor_instance(env, actionExecutor):
    global executor_instance
    if not executor_instance:
        fqcn = env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_EXECUTOR_CLASS, DEFAULT_EXECUTOR_CLASS)
        env.log("Creating a new executor instance of {}".format(fqcn))
        klass = find_class(fqcn)
        executor_instance = klass(env, actionExecutor)
    # NOT THREAD SAFE
    # even if we already had an instance of an executor the choreographe object might have become
    # stale so we refresh it. We only have one executor instance at once so this should be OK
    executor_instance.actionExecutor = actionExecutor
    return executor_instance

'''
Get the instance of the mapper to use
'''
def get_mapper_instance(env):
    global mapper_instance
    if not mapper_instance:
        fqcn = env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_MAPPER_CLASS, DEFAULT_MAPPER_CLASS)
        env.log("Creating a new mapper instance of {}".format(fqcn))
        klass = find_class(fqcn)
        mapper_instance = klass(env)
    return mapper_instance

def run_updaters(env, position, sensors):
    global wanderer_logger
    # do the map update
    mapper = get_mapper_instance(env)
    if mapper:
        try:
            mapper.update(position, sensors)
        except TypeError as e:
            wanderer_logger.error("Error running mapper {0} update: {1}".format(repr(mapper), e))
    
    # run any other updaters
    updater_instances = get_updaters(env)
             
    for updater in updater_instances:
        try:
            updater. update(position, sensors)
        except TypeError as e:
            wanderer_logger.error("Error running updater {0} update: {1}".format(repr(updater), e))
    
def get_updaters(env):
    global updater_instances
    if not updater_instances:
        updater_instances = []
        fqcns = env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_UPDATER_CLASSES)
        if fqcns:
            for fqcn in fqcns:
                env.log("Creating a new updater instance of {}".format(fqcn))
                klass = find_class(fqcn)
                updater = klass(env)
                if updater:
                    updater_instances.append(updater)
    
    return updater_instances

def make_wanderer_environment(box_):
    env = make_environment(box_)
    env.set_application_name(WANDERER_NAME)
    return env

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
Get the entire path
'''
def get_path(env):
    return env.memory.getData(MEM_WALK_PATH)

def set_path(env, path):
    env.memory.insertData(MEM_WALK_PATH, path)

'''
Get the last position the robot was at by looking at the path
'''
def get_last_position(env):
    path = get_path(env)
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
    return env.motion.getPosition("Torso", 1, True)

def save_waypoint(env, waypoint):
    path = get_path(env)
    if path is None:
        path = []
    path.append(waypoint)
    env.log("Path = "+str(path))
    set_path(env, path)

