'''
Created on Feb 9, 2013

@author: dsnowdon
'''

import inspect
import os
import unittest

from wanderer.eventhandlers import *
from wanderer.event import *

class Test(unittest.TestCase):

    def test_is_obstruction(self):
        self.assertTrue(is_obstruction(ObstacleDetected(None, None)), 
                        "should have detected obstruction")

    def test_obstruction_direction(self):
        pass
    
    def test_dispatch(self):
        wanderer = Wanderer(None, None)
        event = ObstacleDetected(None, None)
        wanderer.dispatch(event, None)

    def test_startReturnsActions(self):
        wanderer = Wanderer(None, None)
        actions = wanderer.dispatch(Start(), None)
        self.assertIsNotNone(actions, "dispatch has failed to return an initial action")
        self.assertTrue(len(actions) > 0, "dispatch has returned an empty list of actions")

    def test_Bump(self):
        wanderer = Wanderer(None, None)
        actions = wanderer.dispatch(BumpOccurred('left'), None)
        self.assertTrue(actions[0].distance < 0, "backoff after a bump")
        # TODO: sensibly test this

