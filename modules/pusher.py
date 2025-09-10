import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.database import async_session
from database.keywords import get_user_keywords
from database.keyphrases import get_user_keyphrases
from database.subscriptions import get_all_subscriptions
from models.data.Telegram import TelegramMessage
from utils.posts import is_subsequence, normalize_keywords


class Pusher:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.message_queue = asyncio.Queue()
        self.message_queue_enabled = True

        self.subscriptions_dict = {}

        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.update_subscriptions_dict, 'interval', seconds=30)

    async def new_post(self, username: str, post_text: str, message_link: str):
        text = f"Channel @{username} wrote:\n" + post_text + f"\nLink: {message_link}"
        texts = [text[i:i+4096] for i in range(0, len(text), 4096)]

        if self.subscriptions_dict.get(username) is None:
            logging.error("Channel username is not in database")
            return

        normalized_text = normalize_keywords(post_text)
        logging.info(normalized_text)
        for user_id in self.subscriptions_dict.get(username):
            async with async_session.begin() as sess:
                user_keywords = await get_user_keywords(sess, user_id)
                user_keyphrases = await get_user_keyphrases(sess, user_id)
                
            keywords = user_keywords.normalized_keywords.split(',') if user_keywords and user_keywords.normalized_keywords else None
            keyphrases = user_keyphrases.normalized_keyphrases.split(',') if user_keyphrases and user_keyphrases.normalized_keyphrases else None
            if not (
                (keywords and any(keyword == text for keyword in keywords for text in normalized_text))
                or
                (keyphrases and any(is_subsequence(phrase.split(), normalized_text) for phrase in keyphrases))
            ):
                break
            for text in texts:
                logging.info(f"to {user_id} put {text}")
                await self.message_queue.put(TelegramMessage(user_id=user_id, text=text))

    async def update_subscriptions_dict(self):
        async with async_session.begin() as sess:
            subscriptions = await get_all_subscriptions(sess)

        subscriptions_dict: dict[str, set] = {}
        for subscription in subscriptions:
            if subscriptions_dict.get(subscription.channel) is None:
                subscriptions_dict[subscription.channel] = {
                    subscription.user_id}
            else:
                subscriptions_dict[subscription.channel].add(
                    subscription.user_id)

        self.subscriptions_dict = subscriptions_dict
        logging.info(subscriptions_dict)

    async def start_queue_processing(self):
        self.scheduler.start()

        logging.info("Start pusher")
        
        while self.message_queue_enabled:
            msg: TelegramMessage = await self.message_queue.get()

            try:
                await self.bot.send_message(msg.user_id, msg.text, disable_web_page_preview=True)
            except TelegramRetryAfter as e:
                logging.error(f"Telegram error {e}")
                await asyncio.sleep(60)
                continue
            except TelegramBadRequest as e:
                logging.error(f"Pusher error: {e}")
            except Exception as e:
                logging.error(f"Pusher unknown error: {e}")

            self.message_queue.task_done()

    def stop_queue_processing(self):
        self.message_queue_enable = False
