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
            from util.naoutil import make_environment
        except:
            import sys
            sys.path.append(ALFrameManager.getBehaviorPath(self.behaviorId)+"/src/main/python")         
            from util.naoutil import make_environment
        self.env = make_environment(self)

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
        
       
        event = load_event(self.env)
        wanderer = RandomWalk(self, self.env)
        wanderer.handleEvent(event, None)
