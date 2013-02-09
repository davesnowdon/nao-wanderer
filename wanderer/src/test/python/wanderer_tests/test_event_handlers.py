'''
Created on Feb 9, 2013

@author: dsnowdon
'''

import inspect
import os
import unittest

from wanderer.event_handlers import *

class Test(unittest.TestCase):
    def test_is_obstruction(self):
        self.assertTrue(is_obstruction(ObstacleDetected(None, None)), 
                        "should have detected obstruction")
    def test_obstruction_direction(self):
        pass

if __name__ == '__main__':
    unittest.main()

