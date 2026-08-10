"""
Short, bilingual descriptions for each of the 16 MBTI types.

Kept intentionally concise (per spec: "do not write huge walls of text").
Each type has: personality, strengths, challenges, work_style, communication_style.
"""

from __future__ import annotations

TYPE_DESCRIPTIONS: dict[str, dict[str, dict[str, str]]] = {
    "INTJ": {
        "personality": {"en": "Strategic, independent, and driven by long-term vision.", "ru": "Стратегичный, независимый, нацеленный на долгосрочные цели."},
        "strengths": {"en": "Big-picture thinking, self-discipline, high standards.", "ru": "Видение целого, самодисциплина, высокие стандарты."},
        "challenges": {"en": "Can seem detached; may over-plan instead of acting.", "ru": "Может казаться отстранённым; иногда переизбыток планирования вместо действий."},
        "work_style": {"en": "Prefers autonomy and clear long-term goals over micromanagement.", "ru": "Предпочитает автономию и чёткие долгосрочные цели, не любит микроменеджмент."},
        "communication_style": {"en": "Direct and idea-focused; skips small talk when possible.", "ru": "Прямой, ориентированный на суть; избегает пустых разговоров."},
    },
    "INTP": {
        "personality": {"en": "Curious, analytical, and endlessly interested in how things work.", "ru": "Любопытный, аналитичный, вечно интересуется, как всё устроено."},
        "strengths": {"en": "Original thinking, logical rigor, comfort with complexity.", "ru": "Оригинальное мышление, логическая строгость, спокойствие в сложности."},
        "challenges": {"en": "May struggle to finish projects or communicate reasoning clearly.", "ru": "Может не доводить проекты до конца или сложно объяснять свою логику."},
        "work_style": {"en": "Thrives with open-ended problems and minimal routine.", "ru": "Расцветает в открытых задачах, не любит рутину."},
        "communication_style": {"en": "Precise and exploratory; enjoys debating ideas, not people.", "ru": "Точный, любит исследовать идеи через спор, не переходя на личности."},
    },
    "ENTJ": {
        "personality": {"en": "Decisive, ambitious, and naturally organizes people toward goals.", "ru": "Решительный, амбициозный, умеет организовывать людей вокруг цели."},
        "strengths": {"en": "Leadership, efficiency, confidence under pressure.", "ru": "Лидерство, эффективность, уверенность под давлением."},
        "challenges": {"en": "Can be impatient or overly blunt with slower processes or people.", "ru": "Бывает нетерпеливым или слишком прямолинейным с более медленными людьми и процессами."},
        "work_style": {"en": "Goal-driven, likes owning outcomes and making fast calls.", "ru": "Ориентирован на результат, любит брать ответственность и быстро решать."},
        "communication_style": {"en": "Blunt, structured, and to the point.", "ru": "Прямой, структурированный, без лишних слов."},
    },
    "ENTP": {
        "personality": {"en": "Quick-witted, inventive, and energized by new ideas and debate.", "ru": "Остроумный, изобретательный, заряжается новыми идеями и дискуссиями."},
        "strengths": {"en": "Creative problem-solving, adaptability, persuasive thinking.", "ru": "Креативное решение задач, адаптивность, убедительность."},
        "challenges": {"en": "May lose interest before finishing; can argue for argument's sake.", "ru": "Может терять интерес до завершения дел; иногда спорит ради самого спора."},
        "work_style": {"en": "Best with variety and freedom to explore multiple angles.", "ru": "Лучше всего работает при разнообразии и свободе исследовать разные подходы."},
        "communication_style": {"en": "Playful, fast-moving, likes to challenge assumptions.", "ru": "Игривый, быстрый, любит ставить под сомнение привычные идеи."},
    },
    "INFJ": {
        "personality": {"en": "Insightful, principled, and quietly focused on meaning.", "ru": "Проницательный, принципиальный, тихо сосредоточен на смысле."},
        "strengths": {"en": "Empathy paired with long-term vision; strong sense of purpose.", "ru": "Эмпатия в сочетании с дальновидностью; сильное чувство цели."},
        "challenges": {"en": "Prone to burnout from taking on others' needs; can overanalyze.", "ru": "Склонен к выгоранию, беря на себя чужие проблемы; может переанализировать."},
        "work_style": {"en": "Wants work that feels meaningful, done with minimal conflict.", "ru": "Хочет работу, наполненную смыслом, с минимумом конфликтов."},
        "communication_style": {"en": "Thoughtful and diplomatic; reads between the lines.", "ru": "Вдумчивый и дипломатичный; читает между строк."},
    },
    "INFP": {
        "personality": {"en": "Idealistic, imaginative, and guided by personal values.", "ru": "Идеалистичный, творческий, руководствуется личными ценностями."},
        "strengths": {"en": "Authenticity, creativity, deep empathy for individuals.", "ru": "Искренность, творчество, глубокая эмпатия к людям."},
        "challenges": {"en": "Can take criticism personally; may avoid necessary conflict.", "ru": "Может принимать критику близко к сердцу; избегает нужных конфликтов."},
        "work_style": {"en": "Needs work aligned with personal values, flexible structure.", "ru": "Нужна работа, соответствующая ценностям, с гибкой структурой."},
        "communication_style": {"en": "Warm and reflective; prefers writing to confrontation.", "ru": "Тёплый и рефлексивный; предпочитает письмо конфронтации."},
    },
    "ENFJ": {
        "personality": {"en": "Warm, persuasive, and genuinely invested in others' growth.", "ru": "Тёплый, убедительный, искренне заинтересован в развитии других."},
        "strengths": {"en": "Motivating people, reading a room, natural leadership.", "ru": "Умение мотивировать, чувствовать атмосферу, природное лидерство."},
        "challenges": {"en": "May neglect own needs while caring for everyone else's.", "ru": "Может забывать о своих потребностях, заботясь обо всех остальных."},
        "work_style": {"en": "Thrives leading or mentoring people toward a shared goal.", "ru": "Расцветает, наставляя людей и ведя их к общей цели."},
        "communication_style": {"en": "Encouraging and expressive; naturally rallies a group.", "ru": "Ободряющий, выразительный; естественно объединяет группу."},
    },
    "ENFP": {
        "personality": {"en": "Enthusiastic, imaginative, and drawn to people and possibilities.", "ru": "Восторженный, творческий, тянется к людям и возможностям."},
        "strengths": {"en": "Big ideas, warmth, ability to connect unrelated concepts.", "ru": "Масштабные идеи, теплота, умение находить связи между разным."},
        "challenges": {"en": "Can struggle with follow-through and routine.", "ru": "Может испытывать трудности с доведением дел до конца и рутиной."},
        "work_style": {"en": "Best with variety, people contact, and room for spontaneity.", "ru": "Лучше всего с разнообразием, общением с людьми и местом для спонтанности."},
        "communication_style": {"en": "Animated and warm; talks in possibilities, not just facts.", "ru": "Живой и тёплый; говорит о возможностях, а не только о фактах."},
    },
    "ISTJ": {
        "personality": {"en": "Reliable, methodical, and grounded in facts and duty.", "ru": "Надёжный, методичный, опирается на факты и чувство долга."},
        "strengths": {"en": "Consistency, attention to detail, follow-through.", "ru": "Последовательность, внимание к деталям, доведение дел до конца."},
        "challenges": {"en": "Can resist change or new methods once a system works.", "ru": "Может сопротивляться переменам, если система уже работает."},
        "work_style": {"en": "Prefers clear processes, deadlines, and defined responsibility.", "ru": "Предпочитает чёткие процессы, сроки и зону ответственности."},
        "communication_style": {"en": "Factual and matter-of-fact; says what it does.", "ru": "Фактологичный, по существу; слова расходятся с делом редко."},
    },
    "ISFJ": {
        "personality": {"en": "Caring, dependable, and quietly attentive to others' needs.", "ru": "Заботливый, надёжный, тихо внимателен к нуждам других."},
        "strengths": {"en": "Loyalty, practical helpfulness, strong memory for details.", "ru": "Верность, практическая помощь, хорошая память на детали."},
        "challenges": {"en": "May overcommit and struggle to say no.", "ru": "Может брать на себя слишком много и с трудом отказывать."},
        "work_style": {"en": "Steady and thorough, prefers supporting a team over the spotlight.", "ru": "Стабильный и тщательный, предпочитает поддержку команды, а не быть в центре внимания."},
        "communication_style": {"en": "Gentle and considerate; avoids unnecessary conflict.", "ru": "Мягкий и внимательный; избегает лишних конфликтов."},
    },
    "ESTJ": {
        "personality": {"en": "Organized, decisive, and focused on getting things done properly.", "ru": "Организованный, решительный, сосредоточен на том, чтобы всё было сделано правильно."},
        "strengths": {"en": "Efficient execution, clear standards, dependable leadership.", "ru": "Эффективное исполнение, чёткие стандарты, надёжное лидерство."},
        "challenges": {"en": "Can be rigid about rules or impatient with ambiguity.", "ru": "Может быть слишком жёстким в правилах или нетерпелив к неопределённости."},
        "work_style": {"en": "Structured, results-oriented, likes clear roles and metrics.", "ru": "Структурированный, ориентирован на результат, любит чёткие роли и метрики."},
        "communication_style": {"en": "Direct and practical; states expectations clearly.", "ru": "Прямой и практичный; чётко озвучивает ожидания."},
    },
    "ESFJ": {
        "personality": {"en": "Sociable, supportive, and attentive to group harmony.", "ru": "Общительный, поддерживающий, внимателен к гармонии в группе."},
        "strengths": {"en": "Building community, practical care, strong sense of responsibility.", "ru": "Умение объединять людей, практическая забота, чувство ответственности."},
        "challenges": {"en": "May prioritize others' approval over own needs.", "ru": "Может ставить одобрение других выше своих собственных нужд."},
        "work_style": {"en": "Thrives in cooperative, people-facing roles with clear expectations.", "ru": "Расцветает в командных ролях с общением и чёткими ожиданиями."},
        "communication_style": {"en": "Warm, sociable, values being kept in the loop.", "ru": "Тёплый, общительный, ценит, когда его держат в курсе дел."},
    },
    "ISTP": {
        "personality": {"en": "Practical, calm, and drawn to figuring out how things work.", "ru": "Практичный, спокойный, любит разбираться, как всё устроено."},
        "strengths": {"en": "Hands-on problem-solving, composure under pressure.", "ru": "Практическое решение задач, хладнокровие под давлением."},
        "challenges": {"en": "May avoid discussing feelings or long-term commitments.", "ru": "Может избегать разговоров о чувствах или долгосрочных обязательств."},
        "work_style": {"en": "Prefers independent, hands-on work over meetings and theory.", "ru": "Предпочитает самостоятельную практическую работу собраниям и теории."},
        "communication_style": {"en": "Economical with words; shows rather than tells.", "ru": "Немногословный; скорее покажет, чем расскажет."},
    },
    "ISFP": {
        "personality": {"en": "Gentle, artistic, and guided by personal aesthetics and values.", "ru": "Мягкий, творческий, руководствуется личной эстетикой и ценностями."},
        "strengths": {"en": "Authenticity, sensitivity, quiet adaptability.", "ru": "Искренность, чувствительность, тихая адаптивность."},
        "challenges": {"en": "May avoid conflict even when it needs addressing.", "ru": "Может избегать конфликта, даже когда его нужно решить."},
        "work_style": {"en": "Prefers flexible, low-conflict environments with creative freedom.", "ru": "Предпочитает гибкую среду с минимумом конфликтов и творческой свободой."},
        "communication_style": {"en": "Quiet and genuine; expresses more through action than words.", "ru": "Тихий и искренний; выражает себя больше через действия, чем слова."},
    },
    "ESTP": {
        "personality": {"en": "Energetic, bold, and thrives in the middle of the action.", "ru": "Энергичный, смелый, чувствует себя в своей стихии в гуще событий."},
        "strengths": {"en": "Quick thinking, adaptability, comfort with risk.", "ru": "Быстрое мышление, адаптивность, спокойное отношение к риску."},
        "challenges": {"en": "Can act before thinking through longer-term consequences.", "ru": "Может действовать, не продумав долгосрочные последствия."},
        "work_style": {"en": "Best with fast-paced, hands-on work and real stakes.", "ru": "Лучше всего в динамичной практической работе с реальными ставками."},
        "communication_style": {"en": "Direct, energetic, and to the point.", "ru": "Прямой, энергичный, по существу."},
    },
    "ESFP": {
        "personality": {"en": "Spontaneous, warm, and fully present in the moment.", "ru": "Спонтанный, тёплый, полностью присутствует в моменте."},
        "strengths": {"en": "Enthusiasm, practical empathy, ability to lift a room's mood.", "ru": "Энтузиазм, практическая эмпатия, умение поднять настроение окружающим."},
        "challenges": {"en": "May avoid planning ahead or difficult long-term decisions.", "ru": "Может избегать планирования наперёд или сложных долгосрочных решений."},
        "work_style": {"en": "Thrives with people, variety, and hands-on tasks.", "ru": "Расцветает среди людей, разнообразия и практических задач."},
        "communication_style": {"en": "Lively, expressive, and easy to warm up to.", "ru": "Живой, выразительный, легко располагает к себе."},
    },
}
