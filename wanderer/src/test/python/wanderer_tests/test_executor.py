'''
Created on Feb 20, 2013

@author: dsnowdon
'''
import math
import unittest

from mock import make_mock_environment

from wanderer.wanderer import PlanExecutor, save_plan, load_plan
from wanderer.action import *

class MockActionExecutor(object):
    def do_action(self, action):
        print "MockActionExecutor.do_action() : "+repr(action)
    
    def all_done(self):
        print "MockActionExecutor.all_done()"

class TestExecutor(unittest.TestCase):
    def test_no_plan(self):
        executor = PlanExecutor(make_mock_environment(), MockActionExecutor())
        executor.perform_next_action()

    
    def test_start_plan(self):
        plan = [Turn(math.pi), WalkForwardsIndefinitely()]
        env = make_mock_environment()
        save_plan(env, plan)
        print "Stored plan = "+repr(load_plan(env))
        executor = PlanExecutor(env, MockActionExecutor())
        executor.perform_next_action()
        executor.perform_next_action()
        executor.perform_next_action()

if __name__ == '__main__':
    unittest.main()