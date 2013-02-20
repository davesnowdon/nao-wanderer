'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of events that can occur
'''
from util.general import object_to_json
from robotstate import Sensors

class Event(object):
    def __init__(self):
        super(Event, self).__init__()

    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return object_to_json(self, None)

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        return klass()


class Start(Event):
    def __init__(self):
        super(Start, self).__init__()


class ObstacleDetected(Event):
    def __init__(self, source, sensorData):
        super(ObstacleDetected, self).__init__()
        self.source = source
        self.sensorData = sensorData

    def is_bumper(self):
        return self.source == 'LeftBumper' or self.source == 'RightBumper'

    def to_json(self):
        return object_to_json(self, { 'source': self.source,
                                      'sensorData' : self.sensorData.to_map()})

    @classmethod
    def from_json(klass, json_object):
        print "json_object = "+repr(json_object)
        return klass(json_object['source'], Sensors(json_object['sensorData']))


class FaceDetected(Event):
    def __init__(self, direction):
        super(FaceDetected, self).__init__()
        self.faceDirection = direction


class FaceRecognised(Event):
    def __init__(self):
        super(FaceRecognised, self).__init__()


class ObjectRecognised(Event):
    def __init__(self):
        super(ObjectRecognised, self).__init__()
