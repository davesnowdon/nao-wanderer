'''
Created on Feb 18, 2013

@author: dsnowdon
'''

import unittest
import math

from naoutil.general import object_to_name
from naoutil.jsonobj import to_json_string, from_json_string

from wanderer.action import *

class Test(unittest.TestCase):
    def test_move_json(self):
        action = Move()
        self.json_serialisation(action)

    def test_WalkForwardsIndefinitely_json(self):
        action = WalkForwardsIndefinitely()
        self.json_serialisation(action)

    def test_WalkStraight_json(self):
        action = WalkStraight(0.5)
        self.json_serialisation(action)
        action = WalkStraight(-0.5)
        self.json_serialisation(action)

    def test_WalkSideways_json(self):
        action = WalkSideways(0.5)
        self.json_serialisation(action)

    def test_Turn_json(self):
        action = Turn(math.pi/2)
        self.json_serialisation(action)
        action = Turn(-math.pi/2)
        self.json_serialisation(action)

    def test_Point_json(self):
        action = Point(0.5, 0.75)
        self.json_serialisation(action)

    def test_Wave_json(self):
        action = Wave()
        self.json_serialisation(action)

    def test_Say_json(self):
        action = Say("Hello world")
        self.json_serialisation(action)

    def test_Wait_json(self):
        action = Wait(0.1)
        self.json_serialisation(action)
        action = Wait(10)
        self.json_serialisation(action)

    def test_NullAction_json(self):
        action = NullAction()
        self.json_serialisation(action)

    def json_serialisation(self, ev):
        json = to_json_string(ev)
        print "Serialisation of "+object_to_name(ev)+" = \n"+json
        self.assertIsNotNone(json, "Serialised object should not be None")
        rev = from_json_string(json)
        self.assertTrue(isinstance(rev, ev.__class__))
        self.assertEqual(ev, rev, "Reconstituted object "+repr(rev)+" must equal original "+repr(ev))

if __name__ == '__main__':
    unittest.main()
