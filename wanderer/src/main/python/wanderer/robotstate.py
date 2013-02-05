'''
Created on Feb 4, 2013

@author: dsnowdon

Code handling robot state (sensors, motor current etc)
'''

'''
Current sensor values
'''
class Sensors(object):
    def __init__(self):
        super(Sensors, self).__init__()

'''
Information about motor state, such as current draw
'''
class Motors(object):
    def __init__(self):
        super(Motors, self).__init__()

'''
Information about robot joint angles
'''
class Joints(object):
    def __init__(self):
        super(Joints, self).__init__()
        