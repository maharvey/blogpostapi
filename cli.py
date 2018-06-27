#!/usr/bin/env python3

# implements a simple CLI to test the blog post API

import sys
import argparse
import json
import requests
from pprint import pprint


def do_get(server):
    '''
    print(('curl -i -H "content-type: application/json" '
           '-XGET http://localhost:80/posts'))
    '''

    r = requests.get('http://{}/posts'.format(server))
    pprint(r.json(), indent=4)


def do_post(server, title, body):
    jdata = {'title': title, 'body': body}
    '''
    print(('curl -i -H "content-type: application/json" '
           '-XPOST -d \'{}\' '
           'http://localhost:80/post').format(json.dumps(jdata)))
    '''

    s = json.dumps(jdata)
    r = requests.post('http://{}/post'.format(server),
            headers={'content-type': 'application/json'},
            data=s)
    print(r.status_code)
    if r.status_code >= 400:
        print(r.json())
		

def do_test(server):
	pass # TODO


def main():
    parser = argparse.ArgumentParser(description='create and retrieve blog posts')
    parser.add_argument('--server', metavar='SERVER:PORT', help='specify api host')
    subparsers = parser.add_subparsers(dest='cmd')

    get = subparsers.add_parser('get', help='return all blog posts')

    post = subparsers.add_parser('post', help='create a new blog post')
    post.add_argument('--title', help='title of post', required=True)
    post.add_argument('--body', help='body of post', required=True)

    test = subparsers.add_parser('test', help='run acceptance tests')
	
    args = parser.parse_args(sys.argv[1:])

    if args.server is None:
        server = 'localhost:80'
    else:
        server = args.server

    if args.cmd == None:
        parser.print_help()
    elif args.cmd == 'get':
        do_get(server)
    elif args.cmd == 'post':
        # this is just for testing purposes, to exercise the api
        # don't need to handle multiple lines
        do_post(server, args.title, args.body)
    elif args.cmd == 'test':
        do_test(server)

if __name__ == '__main__':
    main()

