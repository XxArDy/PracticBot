import shutil

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup
from yt_dlp import YoutubeDL

from keyboards import start_keyboard
from main import bot, dp
from states import UserStates
from keyboards import continue_keyboard


@dp.message_handler(Command('start'))
async def start_cmd(message: types.Message):
    await bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}', reply_markup=start_keyboard)


@dp.message_handler(Text(equals=['Найти музику']), state=None)
async def find_music(message: types.Message):
    await message.answer('Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()


@dp.message_handler(state=UserStates.state)
async def find_music(message: types.Message, state: FSMContext):
    await state.finish()
    msg = await bot.send_message(message.chat.id, "Загрузка..")
    try:
        if 'https://' in message.text:
            info = YoutubeDL().extract_info(message.text, download=False)
        else:
            info = YoutubeDL().extract_info(f'ytsearch:{message.text}', download=False)['entries'][0]
        filename = f'musics/{message.from_user.id}/{info["title"]}.mp3'
        YDL_OPTIONS = {'format': 'bestaudio/best',
                       'noplaylist': 'True',
                       'keepvideo': 'False',
                       'outtmpl': filename,
                       'postprocessors': [{
                           'key': 'FFmpegExtractAudio',
                           'preferredcodec': 'mp3',
                           'preferredquality': '192',
                       }],
                       }
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([info['webpage_url']])
        except:
            pass
        await msg.delete()
        await message.reply_audio(open(filename, 'rb'), reply_markup=continue_keyboard)
        shutil.rmtree(f'musics/{message.from_user.id}', ignore_errors=True)
    except:
        await msg.delete()
        await bot.send_message(message.chat.id, f"{message.text} - таку музику не знайдено!")

@dp.callback_query_handler(text = 'continue')
async def continue_music(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id,'Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()