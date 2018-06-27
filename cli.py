#!/usr/bin/env python3

# implements a simple CLI to test the blog post API

import sys
import argparse

def do_get():
    print('do_get')
# TODO

def do_post(title, body):
    print('do_post')
    print('  title: "{}"'.format(title))
    print('  body: "{}"'.format(body))
# TODO


def main():
    parser = argparse.ArgumentParser(description='create and retrieve blog posts')
    subparsers = parser.add_subparsers(dest='cmd')

    get = subparsers.add_parser('get', help='return all blog posts')

    post = subparsers.add_parser('post', help='create a new blog post')
    post.add_argument('--title', help='title of post', required=True)
    post.add_argument('--body', help='body of post', required=True)

    args = parser.parse_args(sys.argv[1:])
    if args.cmd == None:
        parser.print_help()
    elif args.cmd == 'get':
        do_get()
    elif args.cmd == 'post':
        # this is just for testing purposes, to exercise the api
        # don't need to handle multiple lines
        do_post(args.title, args.body)

if __name__ == '__main__':
    main()

