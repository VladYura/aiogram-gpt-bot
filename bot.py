from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import openai
from config import TOKEN, GPT_TOKEN
import logging

openai.api_key = GPT_TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
model_engine = "text-davinci-003"
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет!\nНапиши мне что-нибудь')


@dp.message_handler()
async def process_help_command(message: types.Message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )
    text = completion.choices[0].message.content
    output = "\n".join([text[i:i+55] for i in range(0, len(text), 55)])
    print('-------------------------------------------------------')
    print(f'User - {message.from_user.first_name} {message.from_user.last_name}, id - {message.from_user.id}')
    print(f'\nMessage - {message.text}')
    print(f'\nAnswer:')
    print(output)
    print('-------------------------------------------------------\n')
    text_for_me = f'😑Чел - {message.from_user.first_name} {message.from_user.last_name} задаёт вопрос:\n\n {message.text}'
    await bot.send_message(594875935, text_for_me)
    await bot.send_message(message.from_user.id, completion.choices[0].message.content)


if __name__ == '__main__':
    executor.start_polling(dp)
