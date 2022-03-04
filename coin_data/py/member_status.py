from aiogram import types

from create_bot import bot, dp, chat_id
from keyboards import sub_keyboard, main_keyboard


@dp.callback_query_handler(lambda callback: callback.data == 'check', state='*')
async def check_sub(call: types.CallbackQuery):
    status = await get_member_status(call)
    if status:
        await bot.send_message(call.message.chat.id, "Hi! I am a crypto bot. With my help, you can easily find out about the current state of the cryptocurrency"
                                                     "you are interested in.", reply_markup=main_keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)


async def get_member_status(message):
    try:
        status = (await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id))['status']
        if status == 'left':
            await message.answer(f'You are not subscribed to the {chat_id} channel', reply_markup=sub_keyboard)
            return False
        else:
            return True
    except Exception:
        if type(message) == types.Message:
            await message.answer(f'You have been excluded from the channel. Contact the administrator.')
            return 'excluded'
        elif type(message) == types.CallbackQuery:
            await message.answer("You haven't subscribed to the channel")