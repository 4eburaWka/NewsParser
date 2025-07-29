from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from modules.bot.message_text import *
from modules.bot.services import get_my_subs_service, get_user_keywords_service, set_keywords_service, subscribe_service, unsubscribe_service
from modules.bot.utils import parse_args


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(START_MESSAGE)
    

@router.message(Command('subscribe'))
async def subscribe(message: Message, command: CommandObject):
    args = parse_args(command, 1)
    
    await subscribe_service(message.from_user.id, args)
    
    await message.reply(SUBSCRIBE_SUCCESS)
    for channel in args:
        await message.bot.subscribe_to_channel(channel)
    

@router.message(Command('unsubscribe'))
async def unsubscribe(message: Message, command: CommandObject):
    args = parse_args(command, 1)
    
    await unsubscribe_service(message.from_user.id, args)
    
    await message.reply(UNSUBSCRIBE_SUCCESS)


@router.message(Command('my_subs'))
async def my_subs(message: Message, command: CommandObject):
    channels = await get_my_subs_service(message.from_user.id)
    await message.reply(SUBSCRIBED_TO_MSG + '\n'.join(map(lambda el: el.channel, channels)))


@router.message(Command('set_keywords'))
async def set_keywords(message: Message, command: CommandObject):
    args = parse_args(command, 1)
    
    await set_keywords_service(message.from_user.id, args)
    await message.reply(KEYWORDS_SETTING_SUCCESS)


@router.message(Command('my_keywords'))
async def my_keywords(message: Message, command: CommandObject):
    keywords = await get_user_keywords_service(message.from_user.id)
    await message.reply(USER_KEYWORDS_MSG + ', '.join(keywords.keywords.split(',')))
