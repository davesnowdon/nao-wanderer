'''
Created on Feb 4, 2013

@author: dsnowdon

Representations of actions the robot can take
'''

'''
Abstract class for all actions.
Many actions will be implemented using choreographe boxes and should NOT
implement an execute method, actions that can be performed in pure python
SHOULD implement a method execute(caller, proxies)
'''
class Action(object):
    def __init__(self):
        super(Action, self).__init__()

'''
Abstract base of any action that causes robot to move
'''
class Move(Action):
    def __init__(self):
        super(Move, self).__init__()

class WalkForwardsIndefinitely(Move):
    def __init__(self):
        super(WalkForwardsIndefinitely, self).__init__()

class WalkForwards(Move):
    def __init__(self, distance):
        super(WalkForwards, self).__init__()
        self.distance = distance

class WalkSideways(Move):
    def __init__(self, distance):
        super(WalkSideways, self).__init__()
        self.distance = distance

class Turn(Move):
    def __init__(self, direction):
        super(Turn, self).__init__()
        self.direction = direction

'''
Point at a location
'''
class Point(Action):
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y

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

'''
Wait for a specified number of seconds
'''
class Wait(Action):
    def __init__(self, delaySeconds):
        super(Wait, self).__init__()
        self.delaySeconds = delaySeconds

'''
Does nothing, used when we need an action but don't have anything to do
'''
class NullAction(Action):
    def __init__(self):
        super(NullAction, self).__init__()

