'''
Created on 8 Jun 2013

@author: dsnowdon
'''
import unittest

from mock import make_mock_environment
from wanderer.wanderer import make_updaters

class TestWanderer(unittest.TestCase):


    def test_make_updaters(self):
        env = make_mock_environment()
        updaters = make_updaters(env)
        print "updaters = {}".format(updaters)
        self.assertTrue(updaters, "updaters should not be none")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()