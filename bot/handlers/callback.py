from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from bot.enums import desc, consts
from bot.keyboards import menu
from bot.fsm.states import Page, Analyzer, Parser, Generator
import io
from datetime import datetime, timezone
from database.response import FailedResponse
from bot.keyboards.types import DownloadTypes
from database.methods import Users, UserCompMethods, MaterialMethods

router = Router()


@router.callback_query(F.data == 'profile_menu')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.profile_page)
    await cb.answer()

    response = await UserCompMethods.get_students_names(cb.from_user.id)
    if isinstance(response, FailedResponse):
        return await cb.message.answer(text=response.detail, reply_markup=menu.get_back_keyboard(), parse_mode="html")
    student_names = response.data
    format_names = '\n'.join([f"- {name}" for name in student_names])
    message = f"<b>👨‍🎓 Ваши текущие студенты:</b>\n {format_names}"
    message += "\n\n💡 Для получения информации о профиле студента воспользуйтесь командой <b>/get Имя студента </b>"
    await cb.message.answer(text=message, parse_mode="html", reply_markup=menu.get_back_keyboard())


@router.callback_query(F.data == 'materials_menu')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.profile_page)
    await cb.answer()

    response = await MaterialMethods.get_materials(cb.from_user.id)
    if isinstance(response, FailedResponse):
        return await cb.message.answer(text=response.detail, reply_markup=menu.get_back_keyboard(), parse_mode="html")
    student_names = response.data
    format_names = '\n'.join([f"- <i>{name}</i>" for name in student_names])
    message = f"<b>📚 Ваши текущие материалы:</b>\n {format_names}"
    message += "\n\n💡 Для получения информации о материале воспользуйтесь командой <b>/get_material Имя материала</b>"
    await cb.message.answer(text=message, parse_mode="html", reply_markup=menu.get_back_keyboard())


@router.callback_query(F.data == 'analyz_menu')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.test_analyzer_page)
    await cb.answer()
    await cb.message.answer(text=desc.ANALYZER_DESC, parse_mode='HTML', reply_markup=menu.get_analyzer_start_keyboard())


@router.callback_query(F.data == 'start_analyz')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Analyzer.active_analyzer_page)
    await cb.answer()
    await cb.message.answer(text="📤 <b>Пришлите документ в формате .csv</b>", parse_mode='HTML',
                            reply_markup=menu.get_cancel_keyboard())


@router.callback_query(F.data == 'parser_menu')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.parser_page)
    await cb.answer()
    await cb.message.answer(text=desc.PARSER_DESC, parse_mode='HTML', reply_markup=menu.get_parse_start_keyboard())


@router.callback_query(F.data == 'start_parse')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Parser.active_parser_page)
    await cb.answer()
    await cb.message.answer(text="📤 <b>Пришлите документ в формате .pdf либо .docx.</b>", parse_mode='HTML',
                            reply_markup=menu.get_cancel_keyboard())


@router.callback_query(F.data == 'generate_content_menu')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.generator_content_page)
    await cb.answer()
    await cb.message.answer(text=desc.GENERATOR_DESC, parse_mode='HTML',
                            reply_markup=menu.get_generate_start_keyboard())


@router.callback_query(F.data == 'start_generate')
async def _(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Generator.active_generation_page)
    await cb.answer()
    await cb.message.answer(text="📤 Пришлите <b>имя вашего студента</b> и <b>название материала для подготовки</b>.\n"
                                 "💡 Пример: Никита, Математика", parse_mode='HTML',
                            reply_markup=menu.get_cancel_keyboard())


@router.callback_query(F.data == 'back')
async def document_msg(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.start_page)
    await cb.answer()
    await cb.message.answer(text=consts.START_MESSAGE, parse_mode='HTML', reply_markup=menu.get_start_keyboard())


@router.callback_query(F.data == 'cancel')
async def document_msg(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.start_page)
    await cb.answer("Действие отменено")
    await cb.message.answer(text=consts.START_MESSAGE, parse_mode='HTML', reply_markup=menu.get_start_keyboard())


@router.callback_query(F.data == 'download')
async def document_msg(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    fsm_data = await state.get_data()
    file_text = fsm_data.get("download_text")
    filename = fsm_data.get("download_filename", "Документ")
    if not file_text:
        return await cb.message.answer(text="Невозможно сохранить файл")

    file_bytes = io.BytesIO(file_text.encode('utf-8'))

    await cb.message.answer_document(
        document=BufferedInputFile(file_bytes.read(),
                                   filename=filename),
        caption="<b>✅ Ваш файл готов к установке!</b>\n💡 Не забудьте <b>сохранить его на своем устройстве</b>, чтобы не потерять!",
        parse_mode="html", reply_markup=menu.get_back_keyboard()
    )


@router.callback_query(F.data == 'save_student')
async def document_msg(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.enter_username_student)
    await cb.message.answer(text="<b>Придумайте уникальное имя этому студенту:</b>", parse_mode="html",
                            reply_markup=menu.get_cancel_keyboard())


@router.callback_query(F.data == 'save_material')
async def document_msg(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.set_state(Page.enter_material_name)
    await cb.message.answer(text="<b>Придумайте уникальное название этому материалу:</b>", parse_mode="html",
                            reply_markup=menu.get_cancel_keyboard())
