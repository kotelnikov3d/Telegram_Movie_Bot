# utils/formatters.py
from typing import Dict


def format_movie_message(movie_data: Dict):
    """
    Форматирует сообщение с информацией о фильме.
    :param movie_data: словарь с данными о фильме
    :return: строка с форматированным сообщением
    """
    return (
        f"{'🎬' if movie_data['type'] == 'movie' else '📺'} *{movie_data['name']}* ({movie_data['year']})\n"
        f"⭐ {movie_data['rating']}\n"
        f"🎥 {movie_data['genres']}\n"
        f"🌍 {movie_data['countries']}\n\n"
        f"📖 {movie_data['description']}\n"
    )


def format_favorite_list_message(movie_data: Dict):
    """
    Форматирует сообщение с информацией о фильме.
    :param movie_data: словарь с данными о фильме
    :return: строка с форматированным сообщением
    """
    favorite_list = []
    for movie in movie_data:
        type_icon = '🎬' if movie['type'] == 'movie' else '📺'
        favorite_list.append(f"{type_icon} {movie['name']} ({movie['year']})")

    message = ('Ваш список избранного:\n' + '\n'.join(favorite_list) +
               '\n\nНажмите чтобы посмотреть информацию о фильме👇')
    return message
