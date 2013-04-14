'''
Created on Feb 4, 2013

@author: dsnowdon

Code handling robot state (sensors, motor current etc)
'''

import math

# joint names in same order as returned by ALMotion.getAngles('Body')
JOINT_NAMES = ('HeadYaw', 'HeadPitch', 
               'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 
               'LWristYaw', 'LHand',
               'LHipYawPitch', 'LHipRoll', 'LHipPitch', 
               'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
               'RHipYawPitch', 'RHipRoll', 'RHipPitch', 
               'RKneePitch',  'RAnklePitch', 'RAnkleRoll',
               'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 
               'RWristYaw', 'RHand')

SENSOR_NAMES = ('LeftBumper', 'RightBumper', 'LeftSonar', 'RightSonar')

NAO_SONAR_ANGULAR_SPREAD = math.pi/6
NAO_SONAR_RADIAL_SPREAD = 0.1
NAO_SONAR_MIN_RANGE = 0.25
NAO_SONAR_MAX_RANGE = 2.5

# return the current value of the left ultrasound sensor
def left_sonar(env):
    return env.memory.getData('Device/SubDeviceList/US/Left/Sensor/Value')

#return the current value of the right ultrasound sensor
def right_sonar(env):
    return env.memory.getData('Device/SubDeviceList/US/Right/Sensor/Value')

'''
Model the parameters of an ultrasound sensor
minRange = minimum range at which the sensor is effective
maxRange = maximum range of the sensor
spread = angle (radians) at which the ultrasound spreads
'''
class UltrasoundModel(object):
    def __init__(self, minRange_, maxRange_, angularSpread_, radialSpread_):
        self.minRange = minRange_
        self.maxRange = maxRange_
        self.angularSpread = angularSpread_
        self.radialSpread = radialSpread_

def nao_sonar_model():
    return UltrasoundModel(NAO_SONAR_MIN_RANGE, 
                           NAO_SONAR_MAX_RANGE, 
                           NAO_SONAR_ANGULAR_SPREAD, 
                           NAO_SONAR_RADIAL_SPREAD)

'''
Current sensor values
'''
class Sensors(object):
    def __init__(self, values):
        super(Sensors, self).__init__()
        self.sensors = { }
        for n in SENSOR_NAMES:
            try:
                self.sensors[n] = values[n]
            except KeyError:
                pass

    def __eq__(self, other):
        return self.sensors == other.sensors

    def get_sensor(self, name):
        return self.sensors[name]

    def to_map(self):
        return self.sensors

'''
Information about motor state, such as current draw
'''
class Motors(object):
    def __init__(self, env):
        super(Motors, self).__init__()

'''
Information about robot joint angles
'''
class Joints(object):
    def __init__(self, env):
        super(Joints, self).__init__()
        self.motionProxy = env.motion
    
    def get_joint(self, name):
        return self.joints[name]
    
    def get_joint_angles(self, useSensors):
        angles = self.motionProxy.getAngles("Body", useSensors)
        self.joints = { }
        for n, v in zip(JOINT_NAMES, angles):
            self.joints[n].angle = v
        
