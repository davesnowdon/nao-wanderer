'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of events that can occur
'''

import time

from robotstate import Sensors

class Event(object):
    def __init__(self, timestamp_=None):
        super(Event, self).__init__()
        self.timestamp = timestamp_ if timestamp_ is not None else time.time() 

    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.name() == other.name() and  self.__dict__ == other.__dict__

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return { 'timestamp': self.timestamp }

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['timestamp'])


class Start(Event):
    def __init__(self, timestamp_=None):
        super(Start, self).__init__(timestamp_)


class ObstacleDetected(Event):
    def __init__(self, source_, sensorData_, position_):
        super(ObstacleDetected, self).__init__()
        self.position = position_
        self.source = source_
        self.sensorData = sensorData_

    def is_bumper(self):
        return self.source == 'LeftBumper' or self.source == 'RightBumper'

    def to_json(self):
        # TODO need a better way of handling superclasses with JSON data
        sp = super(ObstacleDetected, self).to_json()
        tp = { 'position' : self.position,
               'source' : self.source,
               'sensorData' : self.sensorData.to_map()}
        return dict(sp.items() + tp.items())

    @classmethod
    def from_json(klass, json_object):
        # TODO need a better way of handling superclasses with JSON data
        obj = klass(json_object['source'], 
                    Sensors(json_object['sensorData']), 
                    json_object['position'])
        obj.timestamp = json_object['timestamp']
        return obj


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
