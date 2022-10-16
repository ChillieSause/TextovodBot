import requests
import json
import html2text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import time

sleep = 0
print('----+= БОТ ЗАПУЩЕН =+----')
BOT_TOKEN = '5703210320:AAHJvckxYDrlfc2ti2_BNYoX3jVayu9kpfQ'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
button_hi = KeyboardButton('/check')
greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)


class Mydialog(StatesGroup):
    otvet = State()

@dp.message_handler(commands=['start'])
async def test(message: types.Message):
    await message.reply('''
Привет, это бот, который поможет тебе расставить знаки препинания в твоих предложениях!
Если у вас есть желание поддержать автора, то есть несколько способов:
	-  На карту: 4377 7200 0124 1017
	-  Ethereum: 0x1AaCeeE23C780b2c3827b0b06Ae94786b613272A
	
[ Бот сделан на основе api  к которому я не имею никакого отношения, возможны ошибки или расстановка точек на месте запятых ]
    ''', reply_markup=greet_kb)

@dp.message_handler()
async def test(message: types.Message):
    if message.text == '/check':
        await message.reply('Отправь предложение на проверку!!')
        await Mydialog.otvet.set()


@dp.message_handler(state=Mydialog.otvet)
async def processMessgae(message: types.Message,  state: FSMContext):
    try:
        await message.answer('Проверяю...')
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = data['text']
            if len(user_message) >= 50:
                sleep = 10
            else:
                sleep = 5
            r = requests.post('https://textovod.com/api/punctuation/user/add', json={"user_id": "195836", "api_key": "935a90b1276e1eaeca4e921ecc31dcf0", "text": user_message})
            time.sleep(sleep)
            data = json.loads(r.text)
            text_id = data['text_id']
            r2 = requests.post('https://textovod.com/api/punctuation/user/status',
                               json={"user_id": "195836", "api_key": "935a90b1276e1eaeca4e921ecc31dcf0",
                                     "text_id": text_id})
            time.sleep(sleep)
            data2 = json.loads(r2.text)
            v = html2text.html2text(data2['punctuation'])
            await message.reply(v)
        await state.finish()
    except Exception as ex:
        await message.answer('Что-то пошло не так, попробуй снова...')



if __name__ == '__main__':
    executor.start_polling(dp)
