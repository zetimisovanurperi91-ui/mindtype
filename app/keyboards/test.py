from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.data.questions import Question
from app.services.localization import t


def question_keyboard(question: Question, session_id: int, language: str) -> InlineKeyboardMarkup:
    rows = []
    for index, option in enumerate(question["options"]):
        text = option["text"].get(language, option["text"]["en"])
        # callback_data carries the session id so an ownership check can
        # reject answers replayed against someone else's session.
        callback_data = f"ans:{session_id}:{question['id']}:{index}"
        rows.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def result_actions_keyboard(language: str, mbti_type: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "result.share_button"), callback_data=f"share:{mbti_type}")],
            [InlineKeyboardButton(text=t(language, "menu.take_test"), callback_data="test:restart")],
            [InlineKeyboardButton(text="◀️ " + t(language, "menu.title"), callback_data="menu:open")],
        ]
    )
