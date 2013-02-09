'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of events that can occur
'''


class Event(object):
    def __init__(self):
        super(Event, self).__init__()

    def name(self):
        return self.__class__.__name__


class ObstacleDetected(Event):
    def __init__(self, source, sensorData):
        super(ObstacleDetected, self).__init__()
        self.source = source
        self.sensorData = sensorData

class FaceDetected(Event):
    def __init__(self, direction):
        super(ObstacleDetected, self).__init__()
        self.faceDirection = direction

class FaceRecognised(Event):
    def __init__(self):
        super(ObstacleDetected, self).__init__()

class ObjectRecognised(Event):
    def __init__(self):
        super(ObstacleDetected, self).__init__()