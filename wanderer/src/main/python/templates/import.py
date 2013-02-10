'''
Created on Feb 10, 2013

@author: dsnowdon
'''

'''
Template code to copy to choreographe boxes to import the necessary modules
'''
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        try:
            from util.naoutil import make_proxies
        except:
            import sys
            sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId)+"/src/main/python")         
            from util.naoutil import make_proxies
        self.proxies = make_proxies()

    def onLoad(self):
        # attributes needed in shuffle mode
        pass

    def onUnload(self):
         #puts code for box cleanup here
        pass

    def onInput_onStart(self):
        hOffset = self.getParameter("horizontalOffset")        
        bCtrBias = self.getParameter("centerBias")        

        try:
            from wanderer.wanderer import *
            from wanderer.event import *
            from wanderer.randomwalk import RandomWalk
            from util.mathutil import to_degrees
            from util.naoutil import *
        except:
            import sys
            sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId)+"/src/main/python")         
            from wanderer.wanderer import *
            from wanderer.event import *
            from wanderer.randomwalk import RandomWalk
            from util.mathutil import to_degrees
            from util.naoutil import *  
        
       
        event = load_event(self.proxies)
        wanderer = RandomWalk(self, self.proxies)
        wanderer.handleEvent(event, None)
