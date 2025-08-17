# dolma_bot.py
# pip install aiogram==3.*

import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8221433172:AAGGhPDFfJxjNKwjtz8yREChnKMMFq39RTE
"

dp = Dispatcher()
router = Router()
dp.include_router(router)


# /start command
@router.message(F.text == "/start")
async def start_cmd(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🥘 Ուտել", callback_data="eat")
    kb.button(text="🚫 Չուտել", callback_data="not_eat")
    await message.answer(
        "👋 Բարև, կեր ամենահամեղ դոլմաները DolmaTopUtelBot-ում 😋",
        reply_markup=kb.as_markup()
    )


# Ուտել սցենար
@router.callback_query(F.data == "eat")
async def eat_dolma(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Այո", callback_data="hungry_yes")
    kb.button(text="❌ Ոչ", callback_data="hungry_no")
    await callback.message.answer(
        "🍽️ Բարիօր ախպեր, սոված ես՞ 🤔",
        reply_markup=kb.as_markup()
    )


# Չուտել սցենար
@router.callback_query(F.data == "not_eat")
async def not_eat_dolma(callback: CallbackQuery):
    await callback.message.answer("🙅‍♂️ Քու հետ մի պյան էն չի ջիգ, տեղերը խառնել ես 🤨")


# hungry_yes → տոլմա սկսելու
@router.callback_query(F.data == "hungry_yes")
async def hungry_yes(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="👨‍🍳 Սարքել", callback_data="cook")
    await callback.message.answer(
        "😎 Մեր Տոլմից լավը չկա ջիգյար, արի սարքենք 💪",
        reply_markup=kb.as_markup()
    )


# hungry_no → գնա
@router.callback_query(F.data == "hungry_no")
async def hungry_no(callback: CallbackQuery):
    await callback.message.answer("🚶 Դե գնա ախպեր, հետո կկյաս որ սոված լես 😅")


# cook → զգուշացում
@router.callback_query(F.data == "cook")
async def cook_dolma(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="➡️ Շարունակենք", callback_data="continue")
    await callback.message.answer(
        "⚠️ Բռատ, զգուշ կլես, տոլմեն չեն խառնմ 🍃",
        reply_markup=kb.as_markup()
    )


# continue → ընտրություն
@router.callback_query(F.data == "continue")
async def continue_dolma(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="🌿 Թփով տոլմա", callback_data="dolma_leaf")
    kb.button(text="🥬 Կյալամով տոլմա", callback_data="dolma_cabbage")
    await callback.message.answer("👇 Ընտրիր տեսակը՝", reply_markup=kb.as_markup())


# leaf/cabbage → counter 1..10
async def countdown(callback: CallbackQuery):
    await callback.message.answer("👌 Լավ ճաշակ ունես, դե արի փորձենք 🙃")
    await asyncio.sleep(1)
    for i in range(1, 11):
        await callback.message.answer(str(i))
        await asyncio.sleep(1)
    kb = InlineKeyboardBuilder()
    kb.button(text="🍴 Փորձել", callback_data="taste")
    await callback.message.answer("Պրոֆա, դե լա 🍽️", reply_markup=kb.as_markup())

@router.callback_query(F.data == "dolma_leaf")
async def dolma_leaf(callback: CallbackQuery):
    await countdown(callback)

@router.callback_query(F.data == "dolma_cabbage")
async def dolma_cabbage(callback: CallbackQuery):
    await countdown(callback)


# taste → այո/ոչ
@router.callback_query(F.data == "taste")
async def taste(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="👍 Այո", callback_data="taste_yes")
    kb.button(text="👎 Ոչ", callback_data="taste_no")
    await callback.message.answer("🤔 Հն, հավանեցիր՞", reply_markup=kb.as_markup())


# taste_yes
@router.callback_query(F.data == "taste_yes")
async def taste_yes(callback: CallbackQuery):
    await callback.message.answer("👏 Մալադեց, համեցեք երբ ուզմեք 🥳")


# taste_no
@router.callback_query(F.data == "taste_no")
async def taste_no(callback: CallbackQuery):
    await callback.message.answer("👀 Աչքիս քու հետ մի պան էն չի 😅")


async def main():
    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
