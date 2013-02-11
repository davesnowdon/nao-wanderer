'''
Created on Feb 10, 2013

@author: dsnowdon

Code that has dependencies on the NAOqi framework
'''

from naoqi import ALProxy

'''
Hold NAO proxies
'''
class Proxies(object):
    def __init__(self, memory, motion, tts):
        #super(Proxies, self).__init__()
        self.memory = memory
        self.motion = motion
        self.tts = tts

'''
Create proxies object.
Needs to be called from a process with an ALBroker running (for example
within choreographe code)
'''
def make_proxies():
    return Proxies(ALProxy("ALMemory"), 
                   ALProxy("ALMotion"), 
                   ALProxy("ALTextToSpeech"))