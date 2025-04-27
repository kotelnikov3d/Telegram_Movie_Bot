from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict


def add_favorite_markup(index: int) -> InlineKeyboardMarkup:
    """
    Создает разметку кнопки для добавления фильма в избранное.

    :param index: Индекс фильма в списке.
    :return: Разметка кнопки для добавления в избранное.
    """
    inline_markup = InlineKeyboardMarkup()
    inline_button1 = InlineKeyboardButton(text="Добавить в избранное", callback_data=f'add_favorite_{index}')
    inline_markup.add(inline_button1)
    return inline_markup


def add_movies_buttons(movie_list: List[Dict], page: int, last_page: int) -> InlineKeyboardMarkup:
    """
    Создает разметку с кнопками для отображения списка фильмов и навигации по страницам.

    :param movie_list: Список фильмов, где каждый фильм представлен словарем с ключами 'name'.
    :param page: Номер текущей страницы.
    :param last_page: Номер последней страницы.
    :return: Разметка с кнопками для фильмов и навигации.
    """
    inline_markup = InlineKeyboardMarkup()
    row = []
    for index, movie in enumerate(movie_list):
        row.append(InlineKeyboardButton(text=movie['name'], callback_data=f'show_movie_{index}'))
        if len(row) == 3:
            inline_markup.row(*row)
            row.clear()

    inline_markup.row(*row)
    if last_page > 0:
        if page == 0:
            nav_buttons = [InlineKeyboardButton(text="След. страница →", callback_data='favorite_next_page')]
        elif page == last_page:
            nav_buttons = [InlineKeyboardButton(text="← Пред. страница", callback_data='favorite_back_page')]
        else:
            nav_buttons = [InlineKeyboardButton(text="← Пред. страница", callback_data='favorite_back_page'),
                           InlineKeyboardButton(text="След. страница →", callback_data='favorite_next_page')]
        inline_markup.row(*nav_buttons)
    return inline_markup
