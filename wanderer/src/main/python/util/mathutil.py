'''
Created on Jan 19, 2013

@author: dsnowdon
'''
import random
import math

FLOAT_CMP_ACCURACY=0.00000001

def to_degrees(rad):
    return rad * 180 / math.pi

def to_radians(deg):
    return deg * math.pi / 180



def feq(a,b):
    return abs(a-b) < FLOAT_CMP_ACCURACY

def is_zero(a):
    return abs(a) < FLOAT_CMP_ACCURACY