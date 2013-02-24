'''
Created on Feb 20, 2013

@author: dsnowdon
'''
import math
import unittest

from mock import make_mock_environment, MockActionExecutor

from wanderer.wanderer import PlanExecutor, save_plan, load_plan
from wanderer.action import *

class TestExecutor(unittest.TestCase):
    def test_no_plan(self):
        actionExecutor = MockActionExecutor()
        executor = PlanExecutor(make_mock_environment(), actionExecutor)
        executor.perform_next_action()
        self.assertEqual(1, actionExecutor.allDoneCount, "all_done() should have been called once")
        self.assertEqual([], actionExecutor.actions, "No actions should have been executed")

    
    def test_start_plan(self):
        actionExecutor = MockActionExecutor()
        plan = [Turn(math.pi), WalkForwardsIndefinitely()]
        env = make_mock_environment()
        save_plan(env, plan)
        print "Stored plan = "+repr(load_plan(env))
        executor = PlanExecutor(env, actionExecutor)
        executor.perform_next_action()
        executor.perform_next_action()
        executor.perform_next_action()
        self.assertEqual(1, actionExecutor.allDoneCount, "all_done() should have been called once")
        self.assertItemsEqual(plan, actionExecutor.actions, "Executed actions should match plan")
        

if __name__ == '__main__':
    unittest.main()