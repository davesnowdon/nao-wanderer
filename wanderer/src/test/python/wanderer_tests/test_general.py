'''
Created on Feb 19, 2013

@author: dsnowdon
'''

import unittest

from util.general import *

'''
Test free functions in general utilities
'''
class TestFreeFunctions(unittest.TestCase):
    def test_fqcn_to_module(self):
        self.assertEqual(FQCN_to_module("wanderer.event.Start"), "wanderer.event")

    def test_fqcn_to_module_no_module(self):
        self.assertIsNone(FQCN_to_module("Start")) 

    def test_fqcn_to_class(self):
        self.assertEqual(FQCN_to_class("wanderer.event.Start"), "Start")

    def test_fqcn_to_class_no_module(self):
        self.assertEqual(FQCN_to_class("Start"), "Start")

    def test_find_class(self):
        self.assertIsNotNone(find_class('wanderer_tests.test_general.JsonTestBase'))

'''
Tests for JSON serialization of custom objects
'''
class JsonTestBase(object):
    def __init__(self):
        super(JsonTestBase, self).__init__()
    
    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return object_to_json(self, None)

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        return klass()

# class using base class JSON support
class JsonNoData(JsonTestBase):
    def __init__(self):
        super(JsonNoData, self).__init__()

# class with additional data to serialise
class JsonWithData(JsonTestBase):
    def __init__(self, source, sensorData):
        super(JsonWithData, self).__init__()
        self.source = source
        self.sensorData = sensorData

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return object_to_json(self, { 'source' : self.source,
                                      'sensorData' : self.sensorData})

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        print "json_object = "+repr(json_object)
        return klass(json_object['source'], json_object['sensorData'])


class TestJson(unittest.TestCase):
    def test_json_serialise_base(self):
        b = JsonTestBase()
        self.json_serialisation(b)

    def test_json_no_data(self):
        b = JsonNoData()
        self.json_serialisation(b)

    def test_json_with_data(self):
        b = JsonWithData('foo', { 'a': 123, 'b' : 456})
        self.json_serialisation(b)

    def json_serialisation(self, ev):
        json = to_json_string(ev)
        print "Serialisation of "+object_to_name(ev)+" = \n"+json
        self.assertIsNotNone(json, "Serialised object should not be None")
        rev = from_json_string(json)
        self.assertTrue(isinstance(rev, ev.__class__))
        self.assertEqual(ev, rev, "Reconstituted object "+repr(rev)+" must equal original "+repr(ev))

    def test_empty_string(self):
        self.assertIsNone(from_json_string(""), "Empty string should return None")

    def test_none(self):
        self.assertIsNone(from_json_string(None), "None should return None")


if __name__ == '__main__':
    unittest.main()