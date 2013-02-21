'''
Created on Feb 20, 2013

@author: dsnowdon
'''
import math
import unittest

from mock import MockBox, make_mock_proxies

from wanderer.wanderer import PlanExecutor, save_plan, load_plan
from wanderer.action import *

class MockActionExecutor(object):
    def do_action(self, action):
        print "MockActionExecutor.do_action() : "+repr(action)
    
    def all_done(self):
        print "MockActionExecutor.all_done()"

class TestExecutor(unittest.TestCase):
    def test_no_plan(self):
        executor = PlanExecutor(MockBox(), make_mock_proxies(), MockActionExecutor())
        executor.perform_next_action()

    
    def test_start_plan(self):
        plan = [Turn(math.pi), WalkForwardsIndefinitely()]
        proxies = make_mock_proxies()
        save_plan(proxies, plan)
        print "Stored plan = "+repr(load_plan(proxies))
        executor = PlanExecutor(MockBox(), proxies, MockActionExecutor())
        executor.perform_next_action()
        executor.perform_next_action()
        executor.perform_next_action()

if __name__ == '__main__':
    unittest.main()