"""
Static question bank for the MBTI test.

Questions are NOT stored in the database (per project spec) - they live here
as plain Python data so they're easy to read, tweak and version-control.

Each question has:
    id:        stable integer id (also used as the FSM progress index)
    axis:      one of "EI", "SN", "TF", "JP"
    text:      {"en": ..., "ru": ...}
    options:   list of dicts, each with:
                   text: {"en": ..., "ru": ...}
                   weights: dict like {"E": 2} or {"I": 1, "E": 1}

Distribution: 4 x EI, 4 x SN, 4 x TF, 3 x JP = 15 questions.
Each option nudges exactly one axis so the scoring engine and the UI both
stay easy to reason about; a handful of options carry a smaller "1" weight
so no single click can swing the whole axis.
"""

from __future__ import annotations

from typing import TypedDict


class Option(TypedDict):
    text: dict[str, str]
    weights: dict[str, int]


class Question(TypedDict):
    id: int
    axis: str
    text: dict[str, str]
    options: list[Option]


QUESTIONS: list[Question] = [
    # ---------------------------------------------------------------- E / I
    {
        "id": 1,
        "axis": "EI",
        "text": {
            "en": "You arrive at a party where you barely know anyone. What do you naturally do?",
            "ru": "Ты приходишь на вечеринку, где почти никого не знаешь. Что ты делаешь?",
        },
        "options": [
            {"text": {"en": "🗣 Start talking to someone right away", "ru": "🗣 Сразу с кем-то заговариваю"}, "weights": {"E": 2}},
            {"text": {"en": "👀 Observe the room first", "ru": "👀 Сначала осматриваюсь"}, "weights": {"I": 2}},
            {"text": {"en": "👤 Look for one person to talk to", "ru": "👤 Ищу одного человека для разговора"}, "weights": {"I": 1}},
            {"text": {"en": "😄 Crack a joke to break the ice", "ru": "😄 Шучу, чтобы разрядить обстановку"}, "weights": {"E": 1}},
        ],
    },
    {
        "id": 2,
        "axis": "EI",
        "text": {
            "en": "After a busy week, what recharges you more?",
            "ru": "После насыщенной недели что восстанавливает тебя больше?",
        },
        "options": [
            {"text": {"en": "🎉 Plans with a group of friends", "ru": "🎉 Встреча с компанией друзей"}, "weights": {"E": 2}},
            {"text": {"en": "🛋 A quiet evening alone", "ru": "🛋 Тихий вечер в одиночестве"}, "weights": {"I": 2}},
            {"text": {"en": "☕️ One-on-one time with a close friend", "ru": "☕️ Время вдвоём с близким другом"}, "weights": {"I": 1}},
            {"text": {"en": "🎶 A high-energy night out", "ru": "🎶 Активный вечер вне дома"}, "weights": {"E": 1}},
        ],
    },
    {
        "id": 3,
        "axis": "EI",
        "text": {
            "en": "In a group brainstorm, you tend to...",
            "ru": "На групповом мозговом штурме ты обычно...",
        },
        "options": [
            {"text": {"en": "💬 Think out loud right away", "ru": "💬 Сразу думаю вслух"}, "weights": {"E": 2}},
            {"text": {"en": "🤔 Think first, speak once it's formed", "ru": "🤔 Сначала обдумываю, потом говорю"}, "weights": {"I": 2}},
            {"text": {"en": "🔁 Build on what others just said", "ru": "🔁 Развиваю чужие идеи"}, "weights": {"E": 1}},
            {"text": {"en": "📝 Jot down thoughts before sharing", "ru": "📝 Записываю мысли перед тем, как поделиться"}, "weights": {"I": 1}},
        ],
    },
    {
        "id": 4,
        "axis": "EI",
        "text": {
            "en": "An unknown number calls your phone. You...",
            "ru": "Тебе звонит незнакомый номер. Ты...",
        },
        "options": [
            {"text": {"en": "📞 Answer right away, curious who it is", "ru": "📞 Сразу отвечаю, интересно кто это"}, "weights": {"E": 2}},
            {"text": {"en": "🔕 Let it go to voicemail", "ru": "🔕 Даю уйти на автоответчик"}, "weights": {"I": 2}},
            {"text": {"en": "💬 Text back asking what's up", "ru": "💬 Пишу в ответ, спрашиваю в чём дело"}, "weights": {"I": 1}},
            {"text": {"en": "🤙 Answer, you're rarely bothered by calls", "ru": "🤙 Отвечаю, звонки меня не напрягают"}, "weights": {"E": 1}},
        ],
    },
    # ---------------------------------------------------------------- S / N
    {
        "id": 5,
        "axis": "SN",
        "text": {
            "en": "Learning something new, you prefer...",
            "ru": "Изучая что-то новое, ты предпочитаешь...",
        },
        "options": [
            {"text": {"en": "📋 Clear step-by-step instructions", "ru": "📋 Чёткую пошаговую инструкцию"}, "weights": {"S": 2}},
            {"text": {"en": "💡 Understanding the big idea first", "ru": "💡 Сначала понять общую идею"}, "weights": {"N": 2}},
            {"text": {"en": "🖐 Trying it hands-on immediately", "ru": "🖐 Сразу пробовать на практике"}, "weights": {"S": 1}},
            {"text": {"en": "🕸 Exploring how it connects to other ideas", "ru": "🕸 Искать связи с другими идеями"}, "weights": {"N": 1}},
        ],
    },
    {
        "id": 6,
        "axis": "SN",
        "text": {
            "en": "A friend tells you about a strange dream they had. You're most interested in...",
            "ru": "Друг рассказывает тебе странный сон. Тебе больше всего интересно...",
        },
        "options": [
            {"text": {"en": "🎬 The literal events that happened", "ru": "🎬 Конкретные события сна"}, "weights": {"S": 2}},
            {"text": {"en": "🔮 What it might symbolically mean", "ru": "🔮 Что это может символизировать"}, "weights": {"N": 2}},
            {"text": {"en": "🖼 How vivid or realistic it felt", "ru": "🖼 Насколько он был ярким и реалистичным"}, "weights": {"S": 1}},
            {"text": {"en": "🌊 The overall feeling behind it", "ru": "🌊 Общее ощущение, которое он оставил"}, "weights": {"N": 1}},
        ],
    },
    {
        "id": 7,
        "axis": "SN",
        "text": {
            "en": "You get a new gadget. You...",
            "ru": "У тебя новый гаджет. Ты...",
        },
        "options": [
            {"text": {"en": "📖 Read the manual and use it as intended", "ru": "📖 Читаешь инструкцию и используешь по назначению"}, "weights": {"S": 2}},
            {"text": {"en": "🎛 Start exploring and improvising", "ru": "🎛 Начинаешь исследовать и импровизировать"}, "weights": {"N": 2}},
            {"text": {"en": "🙋 Ask someone who already knows it", "ru": "🙋 Спрашиваешь того, кто уже разобрался"}, "weights": {"S": 1}},
            {"text": {"en": "🚀 Imagine other things you could do with it", "ru": "🚀 Представляешь, что ещё с ним можно сделать"}, "weights": {"N": 1}},
        ],
    },
    {
        "id": 8,
        "axis": "SN",
        "text": {
            "en": "People are more likely to describe you as...",
            "ru": "Люди скорее опишут тебя как...",
        },
        "options": [
            {"text": {"en": "🔧 Practical and detail-oriented", "ru": "🔧 Практичного и внимательного к деталям"}, "weights": {"S": 2}},
            {"text": {"en": "🎨 Imaginative and idea-driven", "ru": "🎨 Творческого и увлечённого идеями"}, "weights": {"N": 2}},
            {"text": {"en": "🧾 Someone who notices what's actually there", "ru": "🧾 Того, кто замечает реальные детали"}, "weights": {"S": 1}},
            {"text": {"en": "🌌 Someone who sees patterns and possibilities", "ru": "🌌 Того, кто видит закономерности и возможности"}, "weights": {"N": 1}},
        ],
    },
    # ---------------------------------------------------------------- T / F
    {
        "id": 9,
        "axis": "TF",
        "text": {
            "en": "A friend asks for honest feedback on their work. You...",
            "ru": "Друг просит честно оценить его работу. Ты...",
        },
        "options": [
            {"text": {"en": "🎯 Give a direct, honest assessment", "ru": "🎯 Даёшь прямую честную оценку"}, "weights": {"T": 2}},
            {"text": {"en": "💛 Soften it based on how they're feeling", "ru": "💛 Смягчаешь с учётом их чувств"}, "weights": {"F": 2}},
            {"text": {"en": "📐 Focus on what's objectively wrong", "ru": "📐 Фокусируешься на объективных ошибках"}, "weights": {"T": 1}},
            {"text": {"en": "🌱 Focus on encouraging them first", "ru": "🌱 Сначала стараешься их подбодрить"}, "weights": {"F": 1}},
        ],
    },
    {
        "id": 10,
        "axis": "TF",
        "text": {
            "en": "Making a big decision, you lean on...",
            "ru": "Принимая важное решение, ты опираешься на...",
        },
        "options": [
            {"text": {"en": "⚖️ Logic and weighing pros/cons", "ru": "⚖️ Логику и взвешивание плюсов и минусов"}, "weights": {"T": 2}},
            {"text": {"en": "❤️ What feels right for everyone involved", "ru": "❤️ То, что кажется правильным для всех"}, "weights": {"F": 2}},
            {"text": {"en": "📊 Consistent, objective criteria", "ru": "📊 Последовательные объективные критерии"}, "weights": {"T": 1}},
            {"text": {"en": "🤝 Your values and how it affects people", "ru": "🤝 Свои ценности и влияние на людей"}, "weights": {"F": 1}},
        ],
    },
    {
        "id": 11,
        "axis": "TF",
        "text": {
            "en": "Two friends of yours are arguing. You tend to...",
            "ru": "Двое твоих друзей спорят. Ты обычно...",
        },
        "options": [
            {"text": {"en": "🔍 Figure out who's factually correct", "ru": "🔍 Выясняешь, кто прав по фактам"}, "weights": {"T": 2}},
            {"text": {"en": "🩹 Focus on repairing the relationship", "ru": "🩹 Фокусируешься на примирении"}, "weights": {"F": 2}},
            {"text": {"en": "⚙️ Stay neutral and analyze both sides", "ru": "⚙️ Остаёшься нейтральным и анализируешь обе стороны"}, "weights": {"T": 1}},
            {"text": {"en": "🫂 Empathize with whoever seems hurt", "ru": "🫂 Сочувствуешь тому, кому больнее"}, "weights": {"F": 1}},
        ],
    },
    {
        "id": 12,
        "axis": "TF",
        "text": {
            "en": "You'd rather be known as someone who is...",
            "ru": "Тебе важнее, чтобы тебя считали...",
        },
        "options": [
            {"text": {"en": "🏆 Fair and competent", "ru": "🏆 Справедливым и компетентным"}, "weights": {"T": 2}},
            {"text": {"en": "🌸 Warm and caring", "ru": "🌸 Тёплым и заботливым"}, "weights": {"F": 2}},
            {"text": {"en": "📏 Someone who tells it straight", "ru": "📏 Тем, кто говорит прямо"}, "weights": {"T": 1}},
            {"text": {"en": "🕊 Someone who always considers feelings", "ru": "🕊 Тем, кто всегда учитывает чувства"}, "weights": {"F": 1}},
        ],
    },
    # ---------------------------------------------------------------- J / P
    {
        "id": 13,
        "axis": "JP",
        "text": {
            "en": "You have a completely free day tomorrow. What sounds more natural?",
            "ru": "У тебя завтра абсолютно свободный день. Что тебе ближе?",
        },
        "options": [
            {"text": {"en": "📅 I already know what I want to do", "ru": "📅 Я уже знаю, чем займусь"}, "weights": {"J": 2}},
            {"text": {"en": "🎲 I'll decide when the day starts", "ru": "🎲 Решу, когда день начнётся"}, "weights": {"P": 2}},
            {"text": {"en": "🗂 A rough plan, but staying flexible", "ru": "🗂 Примерный план, но с гибкостью"}, "weights": {"J": 1}},
            {"text": {"en": "🌊 I'll probably just follow whatever happens", "ru": "🌊 Скорее всего, просто пойду по течению"}, "weights": {"P": 1}},
        ],
    },
    {
        "id": 14,
        "axis": "JP",
        "text": {
            "en": "A deadline is approaching. You...",
            "ru": "Приближается дедлайн. Ты...",
        },
        "options": [
            {"text": {"en": "✅ Finish early and steadily", "ru": "✅ Заканчиваешь заранее и равномерно"}, "weights": {"J": 2}},
            {"text": {"en": "🔥 Do your best work close to the deadline", "ru": "🔥 Работаешь лучше всего перед самым дедлайном"}, "weights": {"P": 2}},
            {"text": {"en": "☑️ Track progress against a checklist", "ru": "☑️ Отслеживаешь прогресс по чек-листу"}, "weights": {"J": 1}},
            {"text": {"en": "🤞 Trust it'll come together in time", "ru": "🤞 Веришь, что всё сложится вовремя"}, "weights": {"P": 1}},
        ],
    },
    {
        "id": 15,
        "axis": "JP",
        "text": {
            "en": "Your ideal trip looks like...",
            "ru": "Твоё идеальное путешествие — это...",
        },
        "options": [
            {"text": {"en": "🗺 Planned out with a clear itinerary", "ru": "🗺 Чёткий маршрут, спланированный заранее"}, "weights": {"J": 2}},
            {"text": {"en": "🎒 Loose, deciding day by day", "ru": "🎒 Свободное, решения по ходу"}, "weights": {"P": 2}},
            {"text": {"en": "🧭 Mostly planned with room to wander", "ru": "🧭 В основном спланировано, но с местом для импровизации"}, "weights": {"J": 1}},
            {"text": {"en": "🌀 Totally open, see where it goes", "ru": "🌀 Полностью открытое, куда кривая выведет"}, "weights": {"P": 1}},
        ],
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)


def get_question(question_id: int) -> Question | None:
    """Return a question by its 1-based id, or None if out of range."""
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    return None
