from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.database import DBcommands
db = DBcommands()

async def channel(partners):
    channel = InlineKeyboardMarkup()
    for partner in partners:
        son = await db.like_caunt(partner)
        channel.add(InlineKeyboardButton(text=f"{partner} ({son})", callback_data=f"{partner}"))
    return channel

async def channel2(partners):
    btn = InlineKeyboardMarkup()
    for p in partners:
        son = await db.like_caunt(p.partner)
        btn.add(InlineKeyboardButton(text=f"{p.partner} ({son})", callback_data=f"{p.partner}"))
    return btn