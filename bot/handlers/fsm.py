from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from bot.fsm.states import Analyzer, Parser, Page, Generator
from ai_agent.yandex_gpt import generate_comp_profile, generate_theme_blocks, generate_task
from bot.keyboards import menu
from bot.methods import html
import csv
from utils import parser
import io
import re
from datetime import datetime, timezone
from aiogram.exceptions import TelegramBadRequest
from database.methods import UserCompMethods, MaterialMethods
from api.schemas import user_schema as user_m, material_schema as mat
from database.response import FailedResponse
from bot.keyboards.types import DownloadTypes

router = Router()


def escape_markdown_v2(text: str) -> str:
    # Экранируем спецсимволы MarkdownV2
    return re.sub(r'([_\*\[\]\(\)~`>#+\-=|{}.!])', r'\\\1', text)


@router.message(Analyzer.active_analyzer_page)
async def _(message: Message, state: FSMContext):
    try:
        document = message.document
        if not message.document:
            return await message.answer(
                text="📤 Пожалуйста, <b>загрузите документ в формате .csv</b>, а не изображение/текст/аудио.",
                parse_mode="html", reply_markup=menu.get_cancel_keyboard())
        file_name = document.file_name.lower()
        if not file_name.endswith(".csv"):
            return await message.answer(text="📤 <b>Неверный формат файла.</b>\nℹ️ Доступные форматы: .csv",
                                        parse_mode="html", reply_markup=menu.get_cancel_keyboard())
        await message.answer("📈 Начинаю анализ Ваших тестов...\n🚀 Среднее время ответа: <b>5 секунд</b>",
                             parse_mode="html")
        file = await message.bot.download(file=document.file_id, destination=io.BytesIO())
        file.seek(0)  # Возвращаем курсор в начало файла

        # Читаем CSV
        decoded_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(decoded_file)
        data = str(list(reader))
        response_model = generate_comp_profile(data)
        html_response = html.check_html_tags(response_model)

        if html_response:
            filename = f"Профиль компетенций от {datetime.now(tz=timezone.utc).strftime("%d.%m.%Y %H:%M")} UTC.txt"
            await state.update_data({"download_text": html.remove_html_tags(response_model)})
            await state.update_data({"download_filename": filename})
            return await message.answer(text=response_model, parse_mode="html",
                                        reply_markup=menu.get_download_keyboard(download_type=DownloadTypes.ANALYZ))
        return await message.answer(text=html.remove_html_tags(response_model),
                                    reply_markup=menu.get_download_keyboard(download_type=DownloadTypes.ANALYZ))
    except TelegramBadRequest as e:
        print(e)
        await message.answer("Произошла ошибка при попытке выполнить запрос")


@router.message(Parser.active_parser_page)
async def _(message: Message, state: FSMContext):
    document = message.document
    if not message.document:
        return await message.answer(
            text="📤 Пожалуйста, <b>загрузите документ в формате .docx/.pdf</b>, а не изображение/текст/аудио.",
            parse_mode="html", reply_markup=menu.get_cancel_keyboard())
    file_name = document.file_name.lower()
    if (not file_name.endswith(".pdf")) and (not file_name.endswith(".docx")):
        return await message.answer(text="📤 <b>Неверный формат файла.</b>\nℹ️ Доступные форматы: <i>.docx, .pdf</i>",
                                    parse_mode="html", reply_markup=menu.get_cancel_keyboard())
    await message.answer("📈 Начинаю анализ Вашего материала...\n🚀 Среднее время ответа: <b>7 секунд</b>",
                         parse_mode="html")
    file_bytes = io.BytesIO()
    file = await message.bot.download(file=document.file_id, destination=file_bytes)
    file.seek(0)  # Возвращаем курсор в начало файла

    # decoded_file = io.TextIOWrapper(file, encoding='utf-8')
    response = str()
    if file_name.endswith(".pdf"):
        content = parser.read_pdf(file_bytes)
        response = generate_theme_blocks(content)
    elif file_name.endswith(".docx"):
        content = parser.read_docx(file_bytes)
        response = generate_theme_blocks(content)

    filename = f"Обучающий материал от {datetime.now(tz=timezone.utc).strftime("%d.%m.%Y %H:%M")} UTC.txt"
    await state.update_data({"download_text": response.replace("```", "")})
    await state.update_data({"download_filename": filename})
    return await message.answer(text=response, parse_mode="markdown",
                                reply_markup=menu.get_download_keyboard(download_type=DownloadTypes.PARSE))


@router.message(Page.enter_username_student)
async def _(message: Message, state: FSMContext):
    fsm_data = await state.get_data()
    text = fsm_data.get("download_text")

    username = message.text
    model = user_m.UpdateCompProfile(telegram_id=message.from_user.id,
                                     student=username,
                                     profile=text)
    response = await UserCompMethods.update_comp_profile(model)
    if isinstance(response, FailedResponse):
        return await message.answer(text=response.detail, reply_markup=menu.get_cancel_keyboard())
    await state.clear()
    await message.answer(text="Студент успешно добавлен!", reply_markup=menu.get_back_keyboard())


@router.message(Page.enter_material_name)
async def _(message: Message, state: FSMContext):
    fsm_data = await state.get_data()
    text = fsm_data.get("download_text")

    material_name = message.text
    model = mat.AddMaterial(telegram_id=message.from_user.id,
                            material_name=material_name,
                            material=text)
    response = await MaterialMethods.add_material(model)
    if isinstance(response, FailedResponse):
        return await message.answer(text=response.detail, reply_markup=menu.get_cancel_keyboard())
    await state.clear()
    await message.answer(text="Материал успешно добавлен!", reply_markup=menu.get_back_keyboard())


@router.message(Generator.active_generation_page)
async def _(message: Message, state: FSMContext):
    message_text = message.text
    telegram_id = message.from_user.id
    pattern = r'^[A-Za-zА-Яа-яЁё]+, [A-Za-zА-Яа-яЁё]+$'
    true_form = bool(re.match(pattern, message_text))
    if not true_form:
        return await message.answer(text="Вы ввели данные в неверной форме.", reply_markup=menu.get_cancel_keyboard())
    message_split = message_text.split(", ")
    student_profile = await UserCompMethods.get_profile(telegram_id, message_split[0])
    if isinstance(student_profile, FailedResponse):
        return await message.answer(text=student_profile.detail, reply_markup=menu.get_cancel_keyboard())
    material = await MaterialMethods.get_material(telegram_id, message_split[1])
    if isinstance(material, FailedResponse):
        return await message.answer(text=material.detail, reply_markup=menu.get_cancel_keyboard())
    await message.answer(
        text=f"📈 Начинаю генерацию задачи для студента <b>{message_split[0]}</b>...\n🚀 Среднее время ответа: <b>6 секунд</b>",
        parse_mode="html")
    ai_task = generate_task(profile_comp=student_profile.data, material=material.data)

    html_response = html.check_html_tags(ai_task)

    if html_response:
        return await message.answer(text=ai_task, reply_markup=menu.get_back_keyboard(), parse_mode="html")
    return await message.answer(text=html.remove_html_tags(ai_task), reply_markup=menu.get_back_keyboard())
