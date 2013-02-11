'''
Created on Feb 9, 2013

@author: dsnowdon
'''

import inspect
import os
import unittest

from wanderer.randomwalk import *
from wanderer.event import *

from mock import MockBox, make_mock_proxies

class Test(unittest.TestCase):

    def test_is_obstruction(self):
        self.assertTrue(is_obstruction(ObstacleDetected(None, None)), 
                        "should have detected obstruction")

    def test_obstruction_direction(self):
        pass
    
    def test_dispatch(self):
        wanderer = RandomWalk(MockBox(), make_mock_proxies())
        event = ObstacleDetected('LeftBumper', {'LeftBumper':True})
        wanderer.dispatch(event, None)

    def test_startReturnsActions(self):
        wanderer = RandomWalk(MockBox(), make_mock_proxies())
        actions = wanderer.dispatch(Start(), None)
        self.assertIsNotNone(actions, "dispatch has failed to return an initial action")
        self.assertTrue(len(actions) > 0, "dispatch has returned an empty list of actions")

    def test_Bump(self):
        wanderer = RandomWalk(MockBox(), make_mock_proxies())
        actions = wanderer.dispatch(ObstacleDetected('LeftBumper', {'LeftBumper':True}), None)
        self.assertTrue(actions[0].distance < 0, "backoff after a bump")
        # TODO: sensibly test this

if __name__ == '__main__':
    unittest.main()
