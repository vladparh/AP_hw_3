import pytest
from aiogram.filters import Command
from aiogram.methods import SendMessage
from bot import cmd_start
from bot import help_info
from bot import analitics_show
from bot import beginning
from bot import def_conf
from bot import no_detection
from bot import States
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_cmd_start():
    requester = MockedBot(request_handler=MessageHandler(cmd_start, Command(commands=['start'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/start'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Привет! Чтобы узнать доступные команды, введи /help'


@pytest.mark.asyncio
async def test_help_info():
    requester = MockedBot(request_handler=MessageHandler(help_info, Command(commands=['help'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/help'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == '/metrics - метрики модели \n/detect - детектирование объектов на снимке'


@pytest.mark.asyncio
async def test_analitics_show():
    requester = MockedBot(request_handler=MessageHandler(analitics_show, Command(commands=['metrics'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/metrics'))
    answer_message = calls.send_media_group
    print(answer_message)
    assert answer_message is not None


@pytest.mark.asyncio
async def test_beginning():
    requester = MockedBot(request_handler=MessageHandler(beginning, Command(commands=['detect'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/detect'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Загрузите изображение:'


@pytest.mark.asyncio
async def test_def_conf_1():
    requester = MockedBot(request_handler=MessageHandler(def_conf, state=States.choose_conf))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='0.5'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Провести детектирование объектов?'


@pytest.mark.asyncio
async def test_def_conf_2():
    requester = MockedBot(request_handler=MessageHandler(def_conf, state=States.choose_conf))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='1.5'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Число должно быть десятичным от 0 до 1'


@pytest.mark.asyncio
async def test_def_conf_3():
    requester = MockedBot(request_handler=MessageHandler(def_conf, state=States.choose_conf))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='Пять'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Это не число'


@pytest.mark.asyncio
async def test_def_conf_3():
    requester = MockedBot(request_handler=MessageHandler(def_conf, state=States.choose_conf))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='Пять'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Это не число'


@pytest.mark.asyncio
async def test_no_detection():
    requester = MockedBot(request_handler=MessageHandler(no_detection, state=States.start_detect))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='Нет'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Жаль!'





