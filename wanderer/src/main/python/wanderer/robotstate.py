'''
Created on Feb 4, 2013

@author: dsnowdon

Code handling robot state (sensors, motor current etc)
'''

from naoqi import ALProxy

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
    
    def get_sensor(self, name):
        return self.sensors[name]

'''
Information about motor state, such as current draw
'''
class Motors(object):
    def __init__(self, proxies):
        super(Motors, self).__init__()

'''
Information about robot joint angles
'''
class Joints(object):
    def __init__(self, proxies):
        super(Joints, self).__init__()
        self.motionProxy = proxies.motion
    
    def get_joint(self, name):
        return self.joints[name]
    
    def get_joint_angles(self, useSensors):
        angles = self.motionProxy.getAngles("Body", useSensors)
        self.joints = { }
        for n, v in zip(JOINT_NAMES, angles):
            self.joints[n].angle = v
        
