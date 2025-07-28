import logging

from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest

from configs import config
from modules.pusher import Pusher
from database.database import async_session
from database.subscriptions import get_all_subscribed_channels
from utils.posts import preproccess_post


class Client:
    def __init__(self, api_id: int, api_hash: str, pusher: Pusher):
        self.client = TelegramClient("test", api_id, api_hash)
        self.pusher = pusher
        self.pusher.bot.subscribe_to_channel = self.subscribe_to_channel
        
        logging.info("Start client")

        @self.client.on(events.NewMessage)
        async def handler(event):
            try:
                async with async_session.begin() as sess:
                    subscribed_channels_list = await get_all_subscribed_channels(sess)

                current_channel = await event.get_chat()
                if not current_channel.username or current_channel.username not in subscribed_channels_list:
                    return

                await self.pusher.new_post(
                    current_channel.username, 
                    preproccess_post(event.message.text),
                    f"https://t.me/{current_channel.username}/{event.message.id}"
                )
            except Exception as e:
                logging.error(f"Message handler's error: {e}")

    async def subscribe_to_channel(self, channel: str):
        await self.client(JoinChannelRequest(channel))
    
    async def start_client(self):
        await self.client.start()
        await self.client.run_until_disconnected()
