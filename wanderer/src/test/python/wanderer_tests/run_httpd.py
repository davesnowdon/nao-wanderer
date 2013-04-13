'''
Created on 13 Apr 2013

@author: dns
'''

from mock import make_mock_environment
import wanderer.http as http

# TODO turn this into automated test
def main():
    env = make_mock_environment()
    httpd = http.make_server(env, 8080)
    http.start_server(httpd)

if __name__ == '__main__':
    main()