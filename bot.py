import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, FSInputFile
from config_reader import config
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os
import torch
from PIL import Image


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
router = Router()
dp.include_router(router)
conf = 0.25
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
model.to(device)


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


class States(StatesGroup):
    upload_photo = State()
    choose_conf = State()
    start_detect = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Чтобы узнать доступные команды, введи /help")


@dp.message(Command('help'))
async def help_info(message: Message):
    await message.answer('/metrics - метрики модели \n'
                         '/detect - детектирование объектов на снимке')


@dp.message(Command('metrics'))
async def analitics_show(message: Message):
    album_builder = MediaGroupBuilder(
        caption="Метрики модели"
    )
    img_path = 'analitics/'
    for img in os.listdir(img_path):
        album_builder.add(
            type='photo',
            media=FSInputFile(img_path+img)
        )
    await message.answer_media_group(media=album_builder.build())


@router.message(Command('detect'))
async def beginning(message: Message, state: FSMContext):
    await message.answer(text='Загрузите изображение:')
    await state.set_state(States.upload_photo)


@router.message(States.upload_photo, F.photo)
async def upload_photo(message: Message, state: FSMContext, bot: Bot):
    await bot.download(
                        message.photo[-1],
                        destination='photo/image.jpg'
                       )
    await message.answer(text='Отлично! Введите порог уверенности:')
    await state.set_state(States.choose_conf)


@router.message(States.choose_conf, F.text)
async def def_conf(message: Message, state: FSMContext):
    global conf
    try:
        float(message.text)
        if 0.0 < float(message.text) < 1.0:
            conf = float(message.text)
            await message.answer(
                "Провести детектирование объектов?",
                reply_markup=get_yes_no_kb()
            )
            await state.set_state(States.start_detect)
        else:
            await message.answer(text='Число должно быть десятичным от 0 до 1')
    except ValueError:
        await message.answer(text='Это не число')


@router.message(States.start_detect, F.text.lower() == 'да')
async def detection(message: Message, state: FSMContext):
    global model, conf
    model.conf = conf
    await message.answer(
        text='Подождите, происходит детектирование...',
        reply_markup=ReplyKeyboardRemove())
    im = Image.open('photo/image.jpg')
    results = model(im, size=640)
    results.render()
    image = Image.fromarray(results.ims[0])
    image.save('detect/image.jpg')
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('detect/image.jpg'))
    await message.answer(text='Готово!')
    await state.clear()


@router.message(States.start_detect, F.text.lower() == 'нет')
async def no_detection(message: Message, state: FSMContext):
    await message.answer(
        text='Жаль!',
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
