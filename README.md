# Markov
Another IRC bot written in python that sits in a channel and gathers input from stuff the users type, then generates
output based on the Markov stochastic model.

## Requirements
- Python 3.5+
- PostGreSQL 9.x

The bot requires a config.json. Luckily, there's one provided, and all you have to do is just fill it out, change the
name, and the bot will work (provided that you have the two dependencies above satisfied). The bot also requires a
PostgreSQL database (and a user with the appropriate permissions) in order to run at all. There's only one table with
two columns (prefix and suffix), so it's not too complicated.

## TODO:
- Generate output lol