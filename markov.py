#!/usr/bin/env python3

"""Markov chain irc bot written in Python 3."""
import json
import sys
from client import Client


def main():
    try:
        config_file = open('config.json')
        config = json.load(config_file)
    except FileNotFoundError:
        print('Create config.json file!')
        sys.exit(1)

    client = Client(config)
    client.connect(config['server'], config['port'])
    client.handle_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exiting")
