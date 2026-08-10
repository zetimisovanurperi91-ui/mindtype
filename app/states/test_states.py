from aiogram.fsm.state import State, StatesGroup


class LanguageStates(StatesGroup):
    choosing = State()


class TestStates(StatesGroup):
    resume_prompt = State()
    in_progress = State()
