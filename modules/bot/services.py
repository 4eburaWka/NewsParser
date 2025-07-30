from database.database import async_session
from database.keywords import get_user_keywords, set_user_keywords
from database.keyphrases import get_user_keyphrases, set_user_keyphrases
from database.subscriptions import add_subscriptions, del_subscriptions, get_user_subscriptions
from utils.posts import normalize_keywords, normalize_keyphrases


async def subscribe_service(user_id: int, args: list[str]):
    async with async_session.begin() as sess:
        await add_subscriptions(sess, user_id, args)


async def unsubscribe_service(user_id: int, args: list[str]):
    async with async_session.begin() as sess:
        await del_subscriptions(sess, user_id, args)


async def get_my_subs_service(user_id: int):
    async with async_session.begin() as sess:
        return await get_user_subscriptions(sess, user_id)


async def set_keywords_service(user_id: int, keywords: list[str]):
    async with async_session.begin() as sess:
        return await set_user_keywords(sess, user_id, keywords, normalize_keywords(keywords))


async def get_user_keywords_service(user_id: int):
    async with async_session.begin() as sess:
        return await get_user_keywords(sess, user_id)


async def set_keyphrases_service(user_id: int, keyphrases: list[str]):
    async with async_session.begin() as sess:
        return await set_user_keyphrases(sess, user_id, keyphrases, normalize_keyphrases(keyphrases))


async def get_user_keyphrases_service(user_id: int):
    async with async_session.begin() as sess:
        return await get_user_keyphrases(sess, user_id)
