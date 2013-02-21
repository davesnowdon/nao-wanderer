'''
Created on Feb 8, 2013

@author: dns
'''

import sys
import inspect
import json


def class_to_name(klass):
    return klass.__name__

def object_to_name(obj):
    return obj.__class__.__name__

def object_to_FQCN(obj):
    return obj.__module__ + '.' + obj.__class__.__name__

CLASS_TAG = '__class__'
VALUE_TAG = '__value__'

'''
Remove class/function name to leave module name
'''
def FQCN_to_module(s):
    (moduleName, _) = split_FQCN(s)
    return moduleName

'''
Strip module name to leave class/function name
'''
def FQCN_to_class(s):
    (_, className) = split_FQCN(s)
    return className

'''
Split class name from module
'''
def split_FQCN(s):
    if '.' in s:
        return s.rsplit('.', 1)
    else:
        return (None, s)

'''
Look up a class from a FQCN
'''
def find_class(fqcn):
    (moduleName, className) = split_FQCN(fqcn)
    m = None
    if not moduleName is None:
        try:
            m = __import__(moduleName)
        except ImportError:
            print "Unable to import from " + moduleName
    
    #for name, obj in inspect.getmembers(m):
    for name, obj in inspect.getmembers(sys.modules[moduleName]):
        if inspect.isclass(obj) and className == name:
            return obj
        
    raise TypeError("Can't find class " +fqcn)

'''
Functions for clients to call to serialise/unserialise from strings and files

Idea taken from http://getpython3.com/diveintopython3/serializing.html 
and generalised to allow helper functions to be part of the custom classes
and avoid case statements
'''
def to_json_file(obj, fp):
    if not obj is None:
        json.dump(obj, fp, default=to_json_helper)

def to_json_string(obj):
    if obj is None:
        return ""
    else:
        return json.dumps(obj, default=to_json_helper)

def from_json_file(fp):
    return json.load(fp, object_hook=from_json_helper)

def from_json_string(sv):
    if sv is None or sv == "":
        return None
    else:
        return json.loads(sv, object_hook=from_json_helper)

'''
Convenience function to generate dictionary in correct format
'''
def object_to_json(obj, value):
    if value is None:
        return {CLASS_TAG: object_to_FQCN(obj) }
    else:
        return {CLASS_TAG: object_to_FQCN(obj),
                VALUE_TAG: value}

'''
Helper method to generate JSON for custom classes
'''
def to_json_helper(python_object):
    try:
        method = getattr(python_object, 'to_json')
        return method()
    except AttributeError:
        raise TypeError(repr(python_object) + ' is not JSON serializable')

'''
Helper function to detect serialized classes and call from_json on them
to regenerate the class
'''
def from_json_helper(json_object):
    # check whether this is an object we serialised and tagged with the class name
    if CLASS_TAG in json_object:
        fqcn = json_object[CLASS_TAG]
        klass = find_class(fqcn)

        # invoke from_json on target class
        try:
            try:
                json_object = getattr(klass, 'from_json')(json_object[VALUE_TAG])
            except KeyError:
                json_object = getattr(klass, 'from_json')(None)
        except AttributeError:
            # class does not support being reconstituted from JSON
            pass 
    return json_object

