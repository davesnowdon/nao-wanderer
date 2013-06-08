'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math
from random import Random

from naoutil.general import class_to_name
from util.mathutil import is_zero
from robotstate import NAO_SONAR_MIN_RANGE, NAO_SONAR_MAX_RANGE
from event import *
from action import *
from wanderer import Planner, get_current_action, set_current_action, load_plan

class RandomWalk(Planner):

    def __init__(self, env):
        super(RandomWalk, self).__init__(env)
        self.rng = Random()

    def does_event_interrupt_plan(self, event, state):
        return True

    def handleObstacleDetected(self, event, state):
        if event.is_bumper():
            plan = [WalkStraight(-0.2)]
        else:
            plan = []
        (tmin, tmax) = event_to_obstruction_direction(event)
        turn = self.rng.uniform(tmin, tmax)
        self.env.log("Random turn value = {0} from({1},{2})".format(str(turn), str(tmin), str(tmax)))
        plan.append(Turn(turn))
        plan.append(WalkForwardsIndefinitely())
        return plan

    def handleStart(self, event, state):
        direction = math.radians(self.rng.randint(0, 360))
        return [Turn(direction), WalkForwardsIndefinitely()]

    # continue with the action that was in progress
    def handleContinue(self, event, state):
        currentAction = get_current_action(self.env)
        set_current_action(self.env, NullAction())
        return [currentAction]  + load_plan(self.env)
        

    def handleFaceDetected(self, event, state):
        pass

    '''
    Take an event representing an obstruction and work out what
    direction to avoid.

    Returns two angles representing the min & max free orientations
    '''
def event_to_obstruction_direction(event):
    if is_obstruction(event):
        if event.source == 'LeftBumper':
            return (-math.pi, 0.0)
        elif event.source == 'RightBumper':
            return (0.0, math.pi)
        else:
            leftSonar = float(event.sensorData.get_sensor('LeftSonar'))
            rightSonar = float(event.sensorData.get_sensor('RightSonar'))
            smin = min(leftSonar, rightSonar)
            smax = max(leftSonar, rightSonar)
            srange = smax - smin
            if is_zero(srange):
                # there is no difference between the sonar values so there is an obstacle preventing
                # us from moving forward, we need to turn around
                return (math.pi/2, math.pi*1.5)
            else:
                maxRangeDifference = NAO_SONAR_MAX_RANGE - NAO_SONAR_MIN_RANGE
                normLeftSonar = (leftSonar-smin) / maxRangeDifference
                normRightSonar = (rightSonar-smin) / maxRangeDifference
                if normLeftSonar > normRightSonar:
                    degree_of_turn = (1.0-normLeftSonar) * math.pi/2
                    return (degree_of_turn, degree_of_turn+math.pi)
                elif normLeftSonar < normRightSonar:
                    degree_of_turn = (1.0-normRightSonar) * -math.pi/2
                    return (degree_of_turn, degree_of_turn-math.pi)
                else:
                    # treat as obstacle dead ahead (probably shouldn't get here except in case of
                    # float rounding making left and right equal after normalisation)
                    return (math.pi/2, math.pi*1.5)
    else:
        return (-math.pi, math.pi)

def is_obstruction(event):
    return not (event is None) and event.name() == class_to_name(ObstacleDetected)

