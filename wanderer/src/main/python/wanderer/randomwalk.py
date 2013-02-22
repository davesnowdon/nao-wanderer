'''
Created on Feb 8, 2013

@author: dsnowdon
'''
import math
from random import Random

from util.general import class_to_name
from util.mathutil import to_radians
from event import *
from action import *
from wanderer import Planner

class RandomWalk(Planner):

    def __init__(self, env):
        super(RandomWalk, self).__init__(env)
        self.rng = Random()

    def handleObstacleDetected(self, event, state):
        if event.is_bumper():
            plan = [WalkStraight(-0.2)]
        else:
            plan = []
        (tmin, tmax) = event_to_obstruction_direction(event)
        turn = self.rng.uniform(tmin, tmax)
        self.env.log("Random turn value = "+str(turn)+" from ("+str(tmin)+", "+str(tmax)+")")
        plan.append(Turn(turn))
        plan.append(WalkForwardsIndefinitely())
        return plan

    def handleStart(self, event, state):
        direction = to_radians(self.rng.randint(0, 360))
        return [Turn(direction), WalkForwardsIndefinitely()]

    '''
    Take an event representing an obstruction and work out what
    direction to avoid.

    Returns two angles representing the min & max free orientations
    '''
def event_to_obstruction_direction(event):
    if is_obstruction(event):
        if event.source == 'LeftBumper':
            return (0.0, math.pi)
        elif event.source == 'RightBumper':
            return (-math.pi, 0.0)
        else:
            leftSonar = float(event.sensorData.get_sensor('LeftSonar'))
            rightSonar = float(event.sensorData.get_sensor('RightSonar'))
            smin = min(leftSonar, rightSonar)
            smax = max(leftSonar, rightSonar)
            srange = smax - smin
            normLeftSonar = (leftSonar-smin) / srange
            normRightSonar = (rightSonar-smin) / srange
            meanSonar = (normLeftSonar + normRightSonar) / 2.0
            if meanSonar <= 0.001:
                return (-math.pi, math.pi)
            else:
                return ((normLeftSonar-meanSonar-1.0)*math.pi/2.0,
                        (1.0-normRightSonar-meanSonar)*math.pi/2.0)
    else:
        return (-math.pi, math.pi)

def is_obstruction(event):
    return not (event is None) and event.name() == class_to_name(ObstacleDetected)

