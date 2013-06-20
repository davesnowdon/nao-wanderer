'''
Created on 19 May 2013

Sends data and images via HTTP POST requests to enable test data sets to be constructed

@author: davesnowdon
'''

import os
import tempfile
import datetime
import logging
import json

from util.httputil import post_multipart
from wanderer import DEFAULT_CONFIG_FILE, PROPERTY_DATA_COLLECTOR_HOST, PROPERTY_DATA_COLLECTOR_PORT

class DataPoster(object):
    def __init__(self, env):
        super(DataPoster, self).__init__()
        self.env = env
        self.update_count = 0
        self.logger = logging.getLogger("wanderer.dataposter.DataPoster")
        self.host = self.env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_DATA_COLLECTOR_HOST)
        self.port = self.env.get_property(DEFAULT_CONFIG_FILE, PROPERTY_DATA_COLLECTOR_PORT)
        if self.host and self.port:
            self.running = True
    
    def update(self, position, sensors):
        if self.running:
            data = { 'timestamp' : self.timestamp(),
                     'position' : position,
                     'leftSonar' : sensors.get_sensor('LeftSonar'),
                     'rightSonar' : sensors.get_sensor('RightSonar') }
            jstr = json.dumps(data)
        
            self.update_count = self.update_count + 1
            img_bin = self.take_photo()
            img_filename = self.photo_filename()
            params = [('sensordata', jstr),
                      ('update_seq', str(self.update_count))]
            files = [('fileupload', img_filename, img_bin)]

            (code, response_text) = post_multipart(self.host, self.port, '/', params, files)
            if code == 200:
                self.logger.debug("Update sent successfully, file = {}".format(img_filename))
            else:
                self.logger.error("Unable to send file {filename} got error code {code} with text {text}"
                                  .format(filename=img_filename, code=code, text=response_text))
    
    def take_photo(self):
        absoluteFilename = tempfile.mktemp()
        directoryName = os.path.dirname(absoluteFilename) 
        filename = os.path.dirname(absoluteFilename)
        self.env.photoCapture.setResolution(3)
        self.env.photoCapture.setPictureFormat('jpg')
        theFilename = self.env.photoCapture.takePicture(directoryName, filename)
        with open(theFilename[0], "rb") as f:
            img_bin = f.read()
        os.unlink(theFilename[0])
        return img_bin
    
    def photo_filename(self):
        return "{0}.jpg".format(self.timestamp())

    def timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')