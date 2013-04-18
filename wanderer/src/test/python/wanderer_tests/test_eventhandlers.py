'''
Created on Feb 9, 2013

@author: dsnowdon
'''

import inspect
import os
import unittest

from wanderer.randomwalk import *
from wanderer.event import *

from mock import MockBox, make_mock_environment

class Test(unittest.TestCase):
    def setUp(self):
        self.position = [1.0,2.0,3.0,4.0,5.0,6.0]
        self.sensors = Sensors({'LeftBumper':True})

    def test_is_obstruction(self):
        self.assertTrue(is_obstruction(ObstacleDetected(None, None, None)), 
                        "should have detected obstruction")

    def test_dispatch(self):
        wanderer = RandomWalk(make_mock_environment())
        event = ObstacleDetected('LeftBumper', self.sensors, self.position)
        wanderer.dispatch(event, None)

    def test_startReturnsActions(self):
        wanderer = RandomWalk(make_mock_environment())
        actions = wanderer.dispatch(Start(), None)
        self.assertIsNotNone(actions, "dispatch has failed to return an initial action")
        self.assertTrue(len(actions) > 0, "dispatch has returned an empty list of actions")

    def test_Bump(self):
        wanderer = RandomWalk(make_mock_environment())
        actions = wanderer.dispatch(ObstacleDetected('LeftBumper', self.sensors, self.position), None)
        self.assertTrue(actions[0].distance < 0, "backoff after a bump")
        # TODO: sensibly test this

if __name__ == '__main__':
    unittest.main()
