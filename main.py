import bot
from bot import constants

from bot.bot import Bot

if __name__ == '__main__':
    bot.instance = Bot.create()
    bot.instance.load_extensions()
    bot.instance.run(constants.get_token())
