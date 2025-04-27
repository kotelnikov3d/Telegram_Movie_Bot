from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime


# Список типов титулов
TITLE_TYPES = ['фильм', 'сериал']
# Список жанров
GENRES = [
    'комедия',
    'боевик',
    'фантастика',
    'триллер',
    'приключения',
    'фэнтези',
    'мультфильм',
    'ужасы',
    'мелодрама',
    'семейный'
]
# Список рейтингов
RATINGS = ['9-10', '8-10', '7-10', '6-10', '5-10', '4-10', '3-10', '2-10', '1-10']
# Год текущий
cur_year = datetime.now().year
# Список диапазонов годов
YEARS = [f'{x-5}-{x}' for x in range(cur_year, cur_year-31, -5)]
# Список чисел от 1 до 10
NUMBERS = [str(x) for x in range(1, 11)]


def reply_buttons(mode: str) -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с кнопками в зависимости от выбранного режима.

    :param mode: Режим выбора (например, 'types', 'genres', 'ratings', 'years', 'numbers').
    :return: Объект ReplyKeyboardMarkup с кнопками.
    """
    if mode == 'types':
        buttons = TITLE_TYPES
    elif mode == 'genres':
        buttons = GENRES
    elif mode == 'ratings':
        buttons = RATINGS
    elif mode == 'years':
        buttons = YEARS
    elif mode == 'numbers':
        buttons = NUMBERS
    else:
        buttons = []

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        markup.add(KeyboardButton(button))
    return markup
