"""
Rackspace Cloud Monitoring plugin for HTTP requests as an agent.plugin
type of check.

Copyright 2013 Victor Watkins <vic.watkins@rackspace.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import requests
import argparse
import json
import logging
import re
from sys import exit


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', nargs=1,
                    help='Sends the specified data in a POST request to the \
                    HTTP server, in the same way that a browser does when a \
                    user has  filled  in  an  HTML form  and  presses  the \
                    submit button.')
parser.add_argument('-H', '--header', action='append', nargs=1,
                    help='Extra header to use when getting a web page. \
                    You may specify any number of extra headers.')
parser.add_argument('-I', '--head', action='store_true', 
                    help='Fetch the HTTP-header only! HTTP-servers feature \
                    the command HEAD which this uses to get nothing but the \
                    header of a document.')
parser.add_argument('--no-redirect', action='store_false',
                    help='Disallow following redirects')  # backward by design
parser.add_argument('-m', '--match', default='',
                    help='Specify a regular expression to match from the \
                    response body')
parser.add_argument('-k', '--insecure', action='store_false',
                    help='Disable SSL certificate verification')
parser.add_argument('URL', help='The URL to connect to')
args = parser.parse_args()


def gen_headers(argheader):
    
    '''Return a dictionary requests can use to send headers with.
    In other words, translate from argparse to requests lib.
    
    argheader comes from args as [['h1: list'], ['h2: of'], ['h3: lists']].00000
    '''
    
    headers = {}
    
    if argheader:
        for header in argheader:
            h = header[0].split(':')
        
            try:
                k = h[0]
                if h[1][0] == ' ':  # strip out the leading space
                    v = h[1][1:]
                else:
                    v = h[1]
            except IndexError:
                why = "Skipping malformed header: {0}".format(header)
                logging.warning(why)
                continue
        
            headers.update({k: v})
                 

    return headers    


def do_request(url, **kwargs):
    '''Perform a request and return the request object.
    
    Expected kwargs:
    headers: dictionary of extra headers
    data: data to POST with
    head: true or false to do a HEAD with
    redirects: true to allow redirects, false to disallow
    insecure: true to disable ssl certificate verify
    '''

    h = kwargs.get('headers', {})
    
    if kwargs.get('data'):  # hrmmm this strong-arms you into 1 content-type
        r = requests.post(url, 
                          data=json.dumps(kwargs.get('data', {})),
                          headers=h,
                          allow_redirects=kwargs.get('redirects'),
                          verify=kwargs.get('insecure'))
    elif kwargs.get('head'):
        r = requests.head(url, 
                          headers=h,
                          allow_redirects=kwargs.get('redirects'),
                          verify=kwargs.get('insecure'))
    else:
        r = requests.get(url, 
                         headers=h,
                         allow_redirects=kwargs.get('redirects'),
                         verify=kwargs.get('insecure'))
        
    return r


def does_match(pattern, string):
    '''Return a matched string if regex pattern is found in string.'''
    
    m = re.search(pattern, string)
    
    if m and pattern != '':
        return m.group(0)
    else:
        return "NONE"


def print_results(req):
    '''Print the results from a request object into MaaS-like agent plugin 
    formatting.'''
    
    line = "metric {0} {1} {2}"
    
    print("status OK")
    print(line.format("code", "string", req.status_code))
    print(line.format("bytes", "uint32", len(req.text)))
    print(line.format("duration", "double", 
                      req.elapsed.microseconds / 100))
    print(line.format("match", "string", 
                      does_match(args.match, req.text)))


def spawn():

    rargs = {
        'headers': args.header,
        'data': args.data,
        'head': args.head,
        'redirects': args.no_redirect,
        'insecure': args.insecure
    }
    
    try:
        getr = do_request(args.URL, **rargs)
    except Exception as e:
        print("status {0}".format(e))
        exit(1)
    
    print_results(getr) 