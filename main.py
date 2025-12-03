import asyncio
import logging

from aiogram import Bot

from configs import config
from configs.constants import PROD_ENV
from modules.bot.runner import start_bot
from modules.clients import Client
from modules.pusher import Pusher


logging.basicConfig(
    level=logging.INFO if config.ENV == PROD_ENV else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


bot = Bot(config.BOT_TOKEN)
pusher = Pusher(bot)
client = Client(config.API_ID, config.API_HASH, pusher)


async def main():
    bot_task = asyncio.create_task(start_bot(bot))
    pusher_task = asyncio.create_task(pusher.start_queue_processing())
    client_task = asyncio.create_task(client.start_client())

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        bot_task.cancel()
        pusher.scheduler.shutdown()
        pusher.stop_queue_processing()
        pusher_task.cancel()
        client_task.cancel()


asyncio.run(main())
