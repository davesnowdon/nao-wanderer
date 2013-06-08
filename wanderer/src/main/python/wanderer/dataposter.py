'''
Created on 19 May 2013

A mapper that sends data and images via HTTP POST requests
to enable test data sets to be constructed

@author: dsnowdon
'''

import os
import tempfile
import datetime
import logging

from naoutil.jsonobj import to_json_string
from util.httputil import post_multipart


class DataPoster(object):
    def __init__(self, env):
        super(DataPoster, self).__init__()
        self.env = env
        self.update_count = 0
        self.logger = logging.getLogger("naoutil.naoenv.NaoEnvironment")
    
    def update(self, position, sensors):
        self.update_count = self.update_count + 1
        img_bin = self.take_photo()
        img_filename = self.photo_filename()
        params = [('sensor', to_json_string(sensors)),
                  ('position', to_json_string(position)),
                  'update_seq', str(self.update_count)]
        files = [('fileupload', img_filename, img_bin)]
        (code, response_text) = post_multipart("localhost", 8080, '/', params, files)
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
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"