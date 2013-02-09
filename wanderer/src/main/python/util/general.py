'''
Created on Feb 8, 2013

@author: dns
'''

import math
import random

from util.mathutil import to_radians

class Directions:
    Left, Centre, Right = range(1, 4)

def class_to_name(clazz):
    return clazz.__name__

'''
Choose the next direction to head in
'''
def pick_direction(logger, hHeadAngle, obstruction, maxAngle, bCtrBias):
    
    if bCtrBias and hHeadAngle > 0:
        hMax = hOffset * math.cos(hHeadAngle) 
        hMin = (-2 * hOffset) + hMax
    elif bCtrBias and hHeadAngle < 0:
        hMin = -hOffset * math.cos(hHeadAngle) 
        hMax = (2 * hOffset) + hMin
    else:
        hMin = -hOffset
        hMax = hOffset           
    
    # do we need to avoid an obstacle?
    if not obstruction is None:
        if obstruction == Directions.Left:
            logger.log("there is obstruction on right ")
            hMin = 0
        elif obstruction == Directions.Right:
            logger.log("there is obstruction on right ")
            hMax = 0
        elif obstruction == Directions.Centre:
            logger.log("there is obstruction in centre ")
    else:
        logger.log("no obstruction")
    
    logger.log("hMin = " + str(hMin) + ", hMax = " + str(hMax) + ", head angle = " + str(hHeadAngle) + ", head offset = " + str(hOffset))
        
    hDeg = random.uniform(hMin, hMax)
    return to_radians(hDeg)