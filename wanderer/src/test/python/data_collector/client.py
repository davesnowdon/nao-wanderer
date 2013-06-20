'''
Created on 19 May 2013

@author: dns
'''

import sys
import os
import inspect

from util.httputil import post_multipart


def main(argv):
    this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    nao_rel = '../../../../../data/NAO-Robot.jpg'
    nao_abs = os.path.join(this_dir, nao_rel)
    
    params = [('sensordata', 'json goes here')]
    files = [('fileupload', os.path.basename(nao_abs), open(nao_abs, "rb").read())]

    result = post_multipart("localhost", 8080, '/', params, files)
    print result

if __name__ == '__main__':
    main(sys.argv)