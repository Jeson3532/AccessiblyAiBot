from aiogram import F, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.enums import consts
from bot.keyboards import menu

router = Router()

@router.message(CommandStart())
async def cmd_menu(message: Message):
    await message.answer(text="123")


@router.message(F.data == 'profile')
async def profle_message(message: Message):
    await message.answer(text="test")

@router.message(F.data == 'mini-app')
async def profle_message(message: Message):
    webAppInfo = WebAppInfo(url="localhost:8080")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Отправить данные', web_app=webAppInfo))
    await message.answer(text='Привет!', reply_markup=builder.as_markup())

@router.message(F.data == 'courses')
async def profle_message(message: Message):
    await message.answer(text="test")

@router.message(F.data == 'test')
async def profle_message(message: Message):
    await message.answer(text="test")