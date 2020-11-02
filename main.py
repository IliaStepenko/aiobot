import logging
import os
from aiogram import Bot, types, md
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile, ContentTypes
from aiogram.utils.executor import start_webhook
from cv2 import cv2

TOKEN = '1019187234:AAFDX_Omr5ipqZUxjUc7e-HwwqLgENe3Y9E'


WEBHOOK_HOST = 'https://myawesomebot199.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f'Приветствую! Это демонтрационный бот\n',
        parse_mode=types.ParseMode.HTML,
        disable_web_page_preview=True)


async def create_gif_from_image(filename):
    frame = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    res_file_name = f"{filename.replace('.jpg','')}.mp4"
    print(res_file_name)
    frame_rate = [frame for i in range(1, 4)]
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter(res_file_name, fourcc, 1,  (width, height))

    for fr in frame_rate:
        video.write(fr)

    video.release()

    cv2.destroyAllWindows()
    return res_file_name


@dp.message_handler(Command(['gif', 'Gif'], ignore_caption=False), content_types=ContentTypes.PHOTO)
async def echo(message: types.message):
    from_id = message['chat']['id']
    file_name = f'pp1_{from_id}.jpg'
    print(file_name)
    await message.photo[-1].download(file_name)
    video_file_name = await create_gif_from_image(file_name)
    video = InputFile(video_file_name)
    await bot.send_animation(from_id, video, duration=3)




@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)