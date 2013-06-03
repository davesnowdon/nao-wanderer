'''
Created on 19 May 2013

@author: dns
'''

import sys
import os
import inspect
import httplib, mimetypes
import socket

def post_multipart(host, port, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form
    fields.
    files is a sequence of (name, filename, value) elements for data to
    be uploaded as files
    Return the server's response page.
    """

    content_type, body = encode_multipart_formdata(fields, files)
    
    try:
        conn = httplib.HTTPConnection(host, port)
        conn.putrequest('POST', selector)
        conn.putheader('content-type', content_type)
        conn.putheader('content-length', str(len(body)))
        conn.endheaders()
        conn.send(body)
        response = conn.getresponse()
        data = response.read()
        status = response.status
        if  200 == status:
            return (status, data)
        else:
            return (status, None)
    except socket.error:
        print "Connection error"
        return (404, None)

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form
    fields.
    files is a sequence of (name, filename, value) elements for data to
    be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '---------------------------13049614110900'

    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="{}"'.format(key))
        L.append('')
        L.append(value)

    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="{0}";filename="{1}"'.format(key, filename))
        L.append('Content-Type: {}'.format(get_content_type(filename)))
        L.append('')
        L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary={}'.format(BOUNDARY)
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def main(argv):
    this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    nao_rel = '../../../../../data/NAO-Robot.jpg'
    nao_abs = os.path.join(this_dir, nao_rel)
    
    params = [('sensor', 'json goes here')]
    files = [('fileupload', os.path.basename(nao_abs), open(nao_abs, "rb").read())]

    result = post_multipart("localhost", 8080, '/', params, files)
    print result

if __name__ == '__main__':
    main(sys.argv)