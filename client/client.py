"""Client for the markov bot."""

import psycopg2
import pydle
import sys
from typing import List
from link import Link


class Client(pydle.Client):
    def __init__(self, config):
        self.config = config
        super(self.__class__, self).__init__(nickname=config['nick'], username=config['user'], realname=config['real'])
        db_connection_string = 'dbname=\'{}\' user=\'{}\' host=\'localhost\' password=\'{}\'' \
            .format(config['DBName'], config['DBUser'], config['DBPass'])
        try:
            self.db_connection = psycopg2.connect(db_connection_string)
            print('Connected to DB')
            self.cursor = self.db_connection.cursor()
        except:
            print("Can't connect to psql database")
            sys.exit(1)

    def on_connect(self):
        ghost = 'GHOST {} {}'.format(self.config['nick'], self.config['nickservPass'])
        identify = 'IDENTIFY {} {}'.format(self.config['nick'], self.config['nickservPass'])
        for channel in self.config['channels']:
            self.join(channel)
            self.message('NICKSERV', ghost)
            self.message('NICKSERV', identify)

    def on_message(self, target: str, nick: str, line: str):
        command = line.split()[0]
        if nick == 'shane':
            if command == '!disconnect':
                self.disconnect('Exiting...')

        links = split_line(line)
        self.add_links(links)

    def add_links(self, links: List[Link]):
        for link in links:
            statement = 'INSERT INTO markov (prefix, suffix) VALUES (\'{}\', \'{}\')'.format(link.prefix, link.suffix)
            self.cursor.execute(statement)
            self.db_connection.commit()


def split_line(line: str):
    words = line.split()
    return [Link(' '.join(words[i:i+2]), words[i+2]) for i in range(0, len(words)-2)]
