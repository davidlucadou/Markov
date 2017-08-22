# Markov
Another IRC bot written in python that sits in a channel and gathers input from stuff the users type, then generates
output based on the Markov stochastic model.

## Requirements
- Python 3.5+
- PostGreSQL 9.x

The bot requires a config.json. Luckily, there's one provided, and all you have to do is just fill it out, change the
file name, and the bot will work (provided that you have the two dependencies above satisfied). The bot also requires a
PostgreSQL database (and a user with the appropriate permissions) in order to run at all. There's only one table with
two columns (prefix and suffix), so it's not too complicated.

## Running
Obviously make sure you `pip install requirements.txt`, and make sure the config actually has stuff in it and that it's
named `config.json`. If those requirements are fulfilled, just `python3 markov.py` and it should work.

## TODO:
- ~~Generate output lol~~
- Filter inputs to exclude things like urls (or just allow for custom, user-defined filters)
- Add table creation
- Extend the IRC `!<cmd>` commands so you don't have to mess with the actual code to change stuff
- There's probably a better way to handle configuration in Python. Possibly moving config to YAML.
