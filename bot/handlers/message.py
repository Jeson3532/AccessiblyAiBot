from aiogram import F, Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message)
from aiogram.filters.state import StateFilter

from bot.enums import consts
from bot.keyboards import menu
from bot.fsm.states import Page, Analyzer, Parser
from database.methods import UserMethods, UserCompMethods, MaterialMethods
from database.response import FailedResponse
from api.schemas.user_schema import AddUserModel

router = Router()


@router.message(Command(commands=["start", "menu"]))
async def cmd_menu(message: Message):
    user = UserMethods()
    model = AddUserModel(
        telegram_id=message.from_user.id,
    )
    await user.add_user(AddUserModel(telegram_id=message.from_user.id))
    await message.answer(text=consts.START_MESSAGE, reply_markup=menu.get_start_keyboard(), parse_mode="html")


@router.message(Command(commands=["get"]))
async def _(message: Message):
    username = message.text.split(" ")[1]
    response = await UserCompMethods.get_profile(message.from_user.id, username)
    if isinstance(response, FailedResponse):
        return await message.answer(text=response.detail, reply_markup=menu.get_back_keyboard(), parse_mode="html")
    await message.answer(text=str(response.data), reply_markup=menu.get_back_keyboard(), parse_mode="html")


@router.message(Command(commands=["get_material"]))
async def _(message: Message):
    material_name = message.text.split(" ")[1]
    response = await MaterialMethods.get_material(message.from_user.id, material_name)
    if isinstance(response, FailedResponse):
        return await message.answer(text=response.detail, reply_markup=menu.get_back_keyboard(), parse_mode="html")
    await message.answer(text=str(response.data), reply_markup=menu.get_back_keyboard(), parse_mode="html")


@router.message(StateFilter(Page.start_page, None))
async def echo(message: Message, state: FSMContext):
    await message.answer(text=consts.ECHO_MESSAGE)
