#!/usr/bin/env python3

import os
import logging
import http.server
import sqlite3
import json
from collections import OrderedDict, namedtuple

ServerResponse = namedtuple('ServerResponse', 'code data')

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s  %(levelname)-7s  %(message)s')
log = logging.getLogger()
log.debug('logging init')


class BlogDatabase:
    def __init__(self, filename):
        self.filename = filename

    def open(self):
        if not os.path.isfile(self.filename):
            # if database does not exist, create it
            log.info('creating {}'.format(self.filename))
            self.db = sqlite3.connect(self.filename)

            cursor = self.db.cursor()
            log.debug('sqlite3: {}'.format(query))
            query = ('CREATE TABLE posts ('
                     'post_id integer primary key asc autoincrement, '
                     'title string, '
                     'body string);')
            cursor.execute(query)
        else:
            # open existing database
            log.info('opening {}'.format(self.filename))
            self.db = sqlite3.connect(self.filename)

    def close(self):
        log.info('closing {}'.format(self.filename))
        self.db.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def add_entry(self, title, body):
        query = ('INSERT INTO posts (title, body) VALUES (?,?);')
        log.debug('sqlite3: {}'.format(query))

        cursor = self.db.cursor()
        cursor.execute(query, (title, body))
        self.db.commit()

    def get_entries(self):
        cursor = self.db.cursor()
        query = ('SELECT post_id, title, body FROM posts;')
        log.debug('sqlite3: {}'.format(query))

        cursor = self.db.cursor()
        cursor.execute(query)
        # preserve column order in json
        return [OrderedDict([('post_id', x[0]),
                             ('title', x[1]),
                             ('body', x[2])])
                 for x in cursor.fetchall()]

class ApiServer(http.server.BaseHTTPRequestHandler):
    db = None

    def handle_post(self):
        if self.command == 'POST':
            try:
                content_length = int(self.headers.get('content-length', 0))
                content_body = self.rfile.read(content_length)
                log.debug('content-body: {}'.format(content_body))
                data = json.loads(content_body.decode())
                log.debug('data: {}'.format(data))
                self.db.add_entry(data['title'], data['body'])
                return ServerResponse(201, None)
            except ValueError as e:
                return ServerResponse(400, {'message': str(e)})
        else:
            return ServerResponse(400, {'message': 'invalid request'})

    def handle_posts(self):
        if self.command == 'GET':
            data = self.db.get_entries()
            return ServerResponse(200, data)
        else:
            return ServerResponse(400, {'message': 'invalid request'})

    def dispatch(self):
        endpoint = self.path
        if endpoint == '/post':
            resp = self.handle_post()
        elif endpoint == '/posts':
            resp = self.handle_posts()
        else:
            resp = ServerResponse(400, {'message': 'invalid endpoint'})

        self.send_response(resp.code)
        if resp.data is not None:
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(resp.data), 'UTF-8'))

    def do_GET(self):
        self.dispatch()

    def do_POST(self):
        self.dispatch()

def main():
    # using with... helps ensure the database gets closed
    with BlogDatabase('blog.db') as database:
        ApiServer.db = database
        server = http.server.HTTPServer(('localhost', 80), ApiServer)
        log.info('blogpost API server running')
        server.serve_forever()


if __name__ == '__main__':
    main()

