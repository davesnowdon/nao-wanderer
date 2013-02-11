'''
Created on Feb 11, 2013

@author: dsnowdon
'''

from util.naoutil import Proxies

class MockBox(object):
    def __init__(self):
        super(MockBox, self).__init__()

    def log(self, msg):
        pass

class MockMemory(object):
    def __init__(self):
        super(MockMemory, self).__init__()

    def getData(self, name):
        return None
    
    def insertData(self, name, value):
        pass

def make_mock_proxies():
    return Proxies(MockMemory(), 
                   None, 
                   None)