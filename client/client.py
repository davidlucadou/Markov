"""Client for the markov bot."""

import psycopg2
import pydle
import random
import sys
from typing import List
from link import Link


class Client(pydle.Client):
    def __init__(self, config):
        self.config = config
        super(self.__class__, self).__init__(nickname=config['nick'], username=config['user'], realname=config['real'])
        db_connection_string = """dbname=\'{}\' user=\'{}\' host=\'localhost\' password=\'{}\'""" \
            .format(config['DBName'], config['DBUser'], config['DBPass'])
        try:
            self.db_connection = psycopg2.connect(db_connection_string)
            print('Connected to DB')
            self.cursor = self.db_connection.cursor()
        except:
            print("Can't connect to psql database")
            sys.exit(1)
        random.seed()

    def on_connect(self):
        ghost = 'GHOST {} {}'.format(self.config['nick'], self.config['nickservPass'])
        identify = 'IDENTIFY {} {}'.format(self.config['nick'], self.config['nickservPass'])
        for channel in self.config['channels']:
            self.join(channel)
            self.message('NICKSERV', ghost)
            self.message('NICKSERV', identify)

    def on_channel_message(self, target: str, by: str, message: str):
        command = message.split()[0]
        if by == self.config['admin']:
            if command == '!d':
                self.disconnect()

        links = split_line(message)
        self.add_links(links)

        if self.config['posting']:
            if random.randint(0, 100) <= self.config['chance']:
                line = self.generate_line()
                self.message(target, line)

    def on_disconnect(self, expected):
        print('Closing down DB connection...')
        self.cursor.close()
        self.db_connection.close()

    def add_links(self, links: List[Link]):
        for link in links:
            self.cursor.execute("INSERT INTO markov (prefix, suffix) VALUES (%s, %s)", (link.prefix, link.suffix))
            self.db_connection.commit()

    def generate_line(self):
        statement = "SELECT prefix, suffix FROM markov ORDER BY RANDOM() LIMIT 1"
        self.cursor.execute(statement)
        row = self.cursor.fetchone()
        link = Link(row[0], row[1])
        line = [link.prefix, link.suffix]

        for i in range(random.randint(5, self.config['maxLineLength'])):
            link.slide()
            self.cursor.execute("SELECT suffix FROM markov WHERE prefix = %s ORDER BY RANDOM() LIMIT 1", (link.prefix,))
            try:
                row = self.cursor.fetchone()
                link.suffix = row[0]
                line.append(link.suffix)
            except IndexError:
                break

        return ' '.join(line)




def split_line(line: str):
    words = line.split()
    return [Link(' '.join(words[i:i+2]), words[i+2]) for i in range(0, len(words)-2)]
