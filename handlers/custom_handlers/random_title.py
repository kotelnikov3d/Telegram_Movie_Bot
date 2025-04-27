from telebot.types import Message
from loader import bot, UserState
from api.kinopoisk_api import get_title_list
from utils.misc import formatters
from keyboards.inline.inline_markup import add_favorite_markup
from telebot.apihelper import ApiHTTPException


def get_random_title(message: Message, t_type: str) -> None:
    """
    Получает случайный фильм или сериал указанного типа и отправляет информацию пользователю.

    :param message: Объект сообщения от пользователя.
    :param t_type: Тип контента ("movie" для фильмов или "tv-series" для сериалов).
    """
    try:
        title_data = get_title_list(t_type=t_type)
    except ApiHTTPException as exc:
        print(exc)
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте ещё раз')
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['search_result'] = title_data
        print(data)
    try:
        poster_url = title_data[0]['poster']
        caption = formatters.format_movie_message(title_data[0])
        bot.send_photo(
            chat_id=message.chat.id,  # ID чата
            photo=poster_url,  # Ссылка на изображение
            caption=caption,  # Описание под фото
            parse_mode="Markdown",  # Форматирование текста
            reply_markup=add_favorite_markup(0)
        )
    except (IndexError, KeyError) as exc:
        print(exc)
        bot.reply_to(message, 'Произошла ошибка, попробуйте ещё раз')


@bot.message_handler(commands=["random_movie"])
def handle_random_movie(message: Message) -> None:
    """
    Обрабатывает команду /random_movie, отправляя случайный фильм.

    :param message: Объект сообщения от пользователя.
    """
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
    get_random_title(message, 'movie')


@bot.message_handler(commands=["random_series"])
def handle_random_series(message: Message) -> None:
    """
    Обрабатывает команду /random_series, отправляя случайный сериал.

    :param message: Объект сообщения от пользователя.
    """
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
    get_random_title(message, 'tv-series')
