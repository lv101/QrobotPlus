import requests
import json

from nonebot import session

async def _(session):
    bot = session.bot
    await bot.send_private_message(user_id=3457292188, message='nihao')