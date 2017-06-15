#!/usr/bin/env python

from slackbot.bot import Bot
import logging

def main():
    logging.basicConfig()
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()

