# Telegram Movie Bot

## Описание
Этот бот предназначен для поиска фильмов и сериалов. Он позволяет пользователям:
- Найти фильм или сериал по названию.
- Искать фильмы/сериалы по фильтрам (жанр, год, рейтинг и т. д.).
- Получить случайный фильм или сериал.
- Добавлять фильмы и сериалы в избранное.

## Установка и запуск

### Требования
- Python 3.8+
- Установленные зависимости из `requirements.txt`

### Получение токена
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram.
2. Отправьте команду `/newbot` и следуйте инструкциям.
3. Скопируйте полученный токен и сохраните его.
4. Перейдите https://kinopoisk.dev/#api и следуйте инструкциям для получения API ключа.

### Установка зависимостей
```sh
pip install -r requirements.txt
```

Файл `requirements.txt` содержит следующие зависимости:
```
pyTelegramBotAPI==4.26.0
python-dotenv==0.21.1
requests==2.32.3
peewee==3.17.9
```

### Запуск бота
```sh
python main.py
```

## Конфигурация
Создайте файл `.env` и укажите в нём переменные:
```
BOT_TOKEN=ваш_токен_бота
KP_API_KEY=api_ключ_кинопоиска
```

## Функционал
- `/start` - Запуск бота
- `/help` - Список команд
- `/movie_search` - Поиск фильма/сериала по названию
- `/search_by_filter` - Поиск по фильтрам
- `/random_movie` - Получить случайный фильм
- `/random_series` - Получить случайный сериал
- `/favorite` - Список избранного


## Структура проекта
```
├── api/                # Взаимодействие с внешними API
│   ├── __init__.py
│   ├── kinopoisk_api.py
│
├── config_data/        # Конфигурационные файлы
│   ├── __init__.py
│   ├── config.py
│
├── database/           # Работа с базой данных
│   ├── __init__.py
│   ├── models.py
│   ├── my_database.db
│
├── handlers/           # Обработчики команд
│   ├── custom_handlers/
│   │   ├── __init__.py
│   │   ├── exit.py
│   │   ├── favorite.py
│   │   ├── movie_by_filter.py
│   │   ├── movie_search.py
│   │   ├── random_title.py
│   ├── default_handlers/
│   │   ├── __init__.py
│   │   ├── echo.py
│   │   ├── help.py
│   │   ├── start.py
│
├── keyboards/          # Клавиатуры
│   ├── inline/
│   │   ├── __init__.py
│   │   ├── inline_markup.py
│   ├── reply/
│   │   ├── __init__.py
│   │   ├── reply_markup.py
│
├── states/             # Управление состояниями FSM
│   ├── __init__.py
│
├── utils/              # Вспомогательные функции
│   ├── misc/
│   │   ├── __init__.py
│   │   ├── formatters.py
│   ├── __init__.py
│   ├── set_bot_commands.py
│
├── .env.template       # Шаблон переменных окружения
├── .gitignore          # Исключения для Git
├── loader.py           # Загрузка компонентов бота
├── main.py             # Главный файл для запуска бота
├── requirements.txt    # Список зависимостей
└── README.md           # Этот файл
```

## Контакты
Автор: [Kirill Kotelnikov]

## Лицензия
Этот проект распространяется под лицензией MIT.

