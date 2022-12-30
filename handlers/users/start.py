from pprint import pprint
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import CHANNELS
from keyboards.inline.inlineBtn import channel, channel2
from utils.misc.subcription import check

from utils.db_api.database import DBcommands
from data.config import ADMINS
from loader import dp, bot

db = DBcommands()

ONE = [
    "Sizningcha, 2022-yildagi eng muvaffaqiyatli maʼrifiy loyiha qaysi?",
    "“Jadidlar” toʻplami", "“Zakovat” intellektual oʻyini",
    "“Xalq yuragi” hujjatli filmlari",
    "“Wikimarafon” loyihasi",
    "”Izlam” turkumi"
]

TWO = [
    "Sizningcha, 2022-yildagi eng yaxshi oʻzbek filmi qaysi?",
    "“Baron-2”",
    "“101-reys”",
    "“Ayol qismati”",
    " “Abdulla Qodiriy”",
    "“Hayrat”"
]

THREE = [
    "Sizningcha, 2022-yilda eng yaxshi madaniy-maʼrifiy loyihalarni amalga oshirgan tashkilot qaysi?",
    "Madaniyat vazirligi",
    "Turizm va madaniy meros vazirligi",
    "Yoshlar ishlari agentligi",
    "Kinematografiya agentligi",
    "Yozuvchilar uyushmasi",
]
ALL = [ONE, TWO, THREE]


@dp.callback_query_handler()
async def call_data(call: types.CallbackQuery):
    status = await check(user_id=call.from_user.id, channel=CHANNELS)
    if status:
        user = await db.new_user_like(call.data, call.from_user.id)
        if not user:
            await call.answer(text="Ovoz bergansiz ✅")
            return
        try:
            await bot.edit_message_reply_markup(chat_id=CHANNELS, message_id=call.message.message_id,
                                                reply_markup=await channel2(
                                                    await db.get_partners(call.message.message_id)))
        except:
            pass
    else:
        await call.answer(text="Iltimos, oldin kanalga a'zo bo'ling❗️")
    await call.answer(cache_time=1)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        for post in ALL:
            m = await bot.send_message(chat_id=CHANNELS, text=f"{post[0]}", reply_markup=await channel(post[1:]))
            for partner in post[1:]:
                await db.create_partner(m.message_id, partner)
        await message.answer(text="So'rovnomalar yuborildi")
        return
    else:
        await message.answer(text="You have no permessions")
        return
