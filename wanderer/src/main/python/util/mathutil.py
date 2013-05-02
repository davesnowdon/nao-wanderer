'''
Created on Jan 19, 2013

@author: dsnowdon
'''

import math

FLOAT_CMP_ACCURACY=0.00000001

def feq(a,b):
    return abs(a-b) < FLOAT_CMP_ACCURACY

def is_zero(a):
    return abs(a) < FLOAT_CMP_ACCURACY