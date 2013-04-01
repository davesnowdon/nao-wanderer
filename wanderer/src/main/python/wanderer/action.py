'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of actions the robot can take
'''

from naoutil.jsonobj import object_to_json

'''
Abstract class for all actions.
Many actions will be implemented using choreographe boxes and should NOT
implement an execute method, actions that can be performed in pure python
SHOULD implement a method execute(environment)
'''
class Action(object):
    def __init__(self):
        super(Action, self).__init__()

    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.name() == other.name() and  self.__dict__ == other.__dict__

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return { }

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        return klass()


'''
Abstract base of any action that causes robot to move
'''
class Move(Action):
    def __init__(self):
        super(Move, self).__init__()


class WalkForwardsIndefinitely(Move):
    def __init__(self):
        super(WalkForwardsIndefinitely, self).__init__()


class WalkStraight(Move):
    def __init__(self, distance):
        super(WalkStraight, self).__init__()
        self.distance = distance

    def to_json(self):
        return { 'distance': self.distance }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['distance'])


class WalkSideways(Move):
    def __init__(self, distance):
        super(WalkSideways, self).__init__()
        self.distance = distance

    def to_json(self):
        return { 'distance': self.distance }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['distance'])


class Turn(Move):
    def __init__(self, direction):
        super(Turn, self).__init__()
        self.direction = direction

    def to_json(self):
        return { 'direction': self.direction }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['direction'])

'''
Point at a location
'''
class Point(Action):
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y

    def to_json(self):
        return { 'x': self.x, 'y' : self.y }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['x'], json_object['y'])

'''
Perform a wave action
'''
class Wave(Action):
    def __init__(self):
        super(Wave, self).__init__()


'''
Speak some text. The argument is the key to look up a localised string
not the actual string to say.
'''
class Say(Action):
    def __init__(self, textKey):
        super(Say, self).__init__()
        self.textKey = textKey

    def to_json(self):
        return { 'textKey': self.textKey }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['textKey'])


'''
Wait for a specified number of seconds
'''
class Wait(Action):
    def __init__(self, delaySeconds):
        super(Wait, self).__init__()
        self.delaySeconds = delaySeconds

    def to_json(self):
        return { 'delaySeconds': self.delaySeconds }

    @classmethod
    def from_json(klass, json_object):
        return klass(json_object['delaySeconds'])
    

'''
Does nothing, used when we need an action but don't have anything to do
'''
class NullAction(Action):
    def __init__(self):
        super(NullAction, self).__init__()

