from aiogram.fsm.state import State, StatesGroup


class Page(StatesGroup):
    start_page = State()
    profile_page = State()
    test_analyzer_page = State()
    parser_page = State()
    generator_content_page = State()
    enter_username_student = State()
    enter_material_name = State()


class Analyzer(StatesGroup):
    active_analyzer_page = State()


class Parser(StatesGroup):
    active_parser_page = State()


class Generator(StatesGroup):
    active_generation_page = State()
