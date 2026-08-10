# MindType 🧠

I created **MindType**, a Telegram bot that determines a user's MBTI personality type through a short 15-question situational test.

I wanted to build more than just a simple personality quiz. I wanted to create a small, complete service where users can choose their language, answer questions one by one using interactive buttons, receive their four-letter MBTI type, and explore a clear description of their result.

I also added a statistics section where I keep published research data separate from MindType's own live user statistics. This prevents the bot from presenting its own database statistics as if they represented the entire world's population.

I also implemented a protected **Admin Panel** that only I can access. From there, I can monitor user statistics and export data.

### Tech Stack

* Python 3.12+
* aiogram 3
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Pydantic Settings

---

## 1. Installation

I designed the project so that, after the initial setup, I can start it with only two commands:

```bash
docker compose up -d
python main.py
```

`docker compose up -d` starts the local PostgreSQL database.

When I run `python main.py`, the application automatically applies all pending Alembic migrations and then starts the Telegram bot.

I don't need to run:

```bash
alembic upgrade head
```

manually.

Before the first launch, I install the dependencies and create my `.env` file:

```bash
pip install -r requirements.txt
cp .env.example .env
```

Then I fill in the required environment variables.

---

## 2. Environment Configuration

In my `.env` file, I configure three main values:

```env
BOT_TOKEN=123456789:AAAA-your-bot-token-here
DATABASE_URL=postgresql+asyncpg://mindtype:mindtype@localhost:5432/mindtype
ADMIN_IDS=123456789
```

### `BOT_TOKEN`

I get my Telegram bot token from **@BotFather**.

### `DATABASE_URL`

This is the connection URL for my PostgreSQL database.

When I use the PostgreSQL container from `docker-compose.yml`, the default configuration is:

```env
DATABASE_URL=postgresql+asyncpg://mindtype:mindtype@localhost:5432/mindtype
```

### `ADMIN_IDS`

Here I specify my numeric Telegram user ID.

For example:

```env
ADMIN_IDS=123456789
```

If I want multiple administrators:

```env
ADMIN_IDS=111111111,222222222
```

I intentionally don't hardcode administrator IDs inside the source code.

Access control is centralized in:

```text
app/services/admin_service.py
```

using the:

```text
is_admin()
```

function.

All administrative handlers use this permission check.

---

## 3. Starting MindType

After configuring `.env`, I start PostgreSQL:

```bash
docker compose up -d
```

Then I start the bot:

```bash
python main.py
```

When everything starts successfully, I see logs similar to:

```text
INFO | mindtype | Applying database migrations...
INFO | mindtype | Migrations applied.
INFO | mindtype | MindType bot starting...
```

After that, I open my bot in Telegram and send:

```text
/start
```

---

## 4. Admin Panel

I designed the Admin Panel so that regular users don't even see administrative features.

Access is controlled through:

```env
ADMIN_IDS=123456789
```

If my Telegram ID is included in `ADMIN_IDS`, I can open:

```text
/admin
```

or access the panel through the bot menu.

I see:

```text
👑 Admin Panel
```

Regular users:

* don't see the Admin Panel button;
* cannot access administrative functions;
* receive:

```text
❌ Access denied.
```

if they try to use `/admin`.

This means that both the interface and the actual backend permission check protect the administration area.

---

# 5. Project Structure

I separated the project into several layers so that Telegram handlers, business logic, and database operations don't become mixed together.

```text
mindtype/
├── app/
│   ├── bot.py
│   ├── config.py
│   ├── middlewares.py
│   │
│   ├── handlers/
│   │   ├── start.py
│   │   ├── test.py
│   │   ├── result.py
│   │   ├── statistics.py
│   │   ├── admin.py
│   │   └── common.py
│   │
│   ├── keyboards/
│   │
│   ├── services/
│   │   ├── mbti_engine.py
│   │   ├── statistics_service.py
│   │   ├── localization.py
│   │   └── admin_service.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   ├── states/
│   │
│   ├── data/
│   │   ├── questions.py
│   │   ├── type_descriptions.py
│   │   └── sources.py
│   │
│   └── locales/
│       ├── ru.json
│       └── en.json
│
├── migrations/
├── tests/
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── main.py
└── README.md
```

### `handlers/`

I use the handlers to process Telegram interactions such as:

* `/start`;
* language selection;
* starting the test;
* answering questions;
* displaying results;
* viewing statistics;
* opening the Admin Panel.

I keep complex business logic and SQL queries outside the handlers.

### `services/`

This layer contains the main application logic.

For example:

```text
mbti_engine.py
```

contains the MBTI scoring logic.

```text
statistics_service.py
```

handles the statistics logic.

### `database/`

This layer contains my database models and repositories.

I keep SQLAlchemy-related database operations inside the repositories so that Telegram handlers don't interact with the database directly.

### `data/`

This directory contains the content used by the application.

```text
questions.py
```

contains the 15-question test.

```text
type_descriptions.py
```

contains descriptions for all 16 MBTI types.

```text
sources.py
```

contains the sources used for the research statistics.

### `locales/`

I use separate localization files for:

```text
ru.json
en.json
```

This allows the same bot to work in both Russian and English.

---

# 6. How the Test Works

I created the test around **15 situational questions**.

Users don't need to type their answers.

Each question appears individually:

```text
Question 7 / 15
███████░░░░░░░░

[ Answer option 1 ]
[ Answer option 2 ]
[ Answer option 3 ]
[ Answer option 4 ]
```

The user simply selects the answer that fits them best.

After each answer, the next question appears automatically.

Once all 15 questions have been answered, my scoring engine calculates the result and determines the user's MBTI type.

For example:

```text
INTJ
```

or:

```text
ENFP
```

The result is then saved to the database and displayed to the user.

---

# 7. Results

After completing the test, I show the user:

* their four-letter MBTI type;
* the distribution across the four MBTI dimensions;
* a short personality description;
* additional characteristics;
* a clear disclaimer explaining that the result is not a psychological diagnosis.

For example:

```text
🧠 Your type: INTJ

I — 72%
N — 81%
T — 68%
J — 75%
```

I also save the result in the database.

If the user later opens:

```text
📊 My result
```

they can see their latest result again.

If they retake the test, the new result is saved separately instead of replacing the previous result.

---

# 8. Statistics

I separated the statistics into two independent categories.

### 🌍 Research Data

These are published research statistics.

I don't want to invent statistics, so I keep the source information separate and clearly label the data.

In the current version, I use the published estimated MBTI frequency table from the **Myers & Briggs Foundation**.

These figures are based on specific MBTI data samples and should not be interpreted as an exact representation of the world's population.

### 🤖 MindType Statistics

This is the live statistics generated from my own bot database.

For example:

```text
👥 Total users: 1,284

Most common types:

ENFP — 14.2%
INFP — 12.8%
INTJ — 10.4%
ISFJ — 9.7%
...
```

These numbers are calculated directly from MindType's database.

I intentionally keep research statistics and MindType user statistics visually and conceptually separate so users don't confuse the two.

---

# 9. What I Test After Launch

After starting the bot, I test the complete user flow:

* [ ] `/start` shows the language selector for a new user
* [ ] the selected language is saved
* [ ] running `/start` again opens the main menu
* [ ] 🧠 `Take the test` starts the test
* [ ] all 15 questions are displayed
* [ ] questions appear one at a time
* [ ] answers are selected using buttons
* [ ] a progress indicator is displayed
* [ ] the result appears after question 15
* [ ] the result contains a four-letter MBTI type
* [ ] the dimension scores are displayed
* [ ] the result is saved to the database
* [ ] `📊 My result` displays the latest result
* [ ] retaking the test creates a new result
* [ ] previous results remain stored
* [ ] 🌍 `Statistics` separates research data from MindType statistics
* [ ] `/start` during an active test offers the option to continue
* [ ] regular users cannot see the Admin Panel
* [ ] `/admin` is blocked for non-admin users
* [ ] my configured Telegram ID can access the Admin Panel
* [ ] 📥 `Export CSV` sends a CSV file to the administrator

---

# 10. Limitations and Honest Caveats

I consider MindType an MVP and a practical learning project.

The MBTI result should not be treated as a medical or psychological diagnosis.

The research statistics also should not be interpreted as an exact description of the world's population because they are based on specific published samples.

The current database schema already contains the `StatisticSource` table, but the MVP currently loads its small curated set of statistics directly from:

```text
app/data/sources.py
```

This keeps the initial setup simple and avoids requiring an additional database seeding step.

In the future, I can expand the statistics system, add more research sources, and move the statistical data into a fully populated database table.
