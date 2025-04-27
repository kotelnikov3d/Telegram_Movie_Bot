from telebot.types import Message, ReplyKeyboardRemove
from loader import bot, UserState
from api.kinopoisk_api import get_title_list
from utils.misc import formatters
from keyboards.reply.reply_markup import reply_buttons
from keyboards.inline.inline_markup import add_favorite_markup


@bot.message_handler(commands=["movie_by_filter"])
def handle_movie_search_by_filter(message: Message) -> None:
    """
    Запускает процесс фильтрации фильмов.
    """
    bot.reply_to(message, "Выберите фильм или сериал", reply_markup=reply_buttons('types'))
    bot.set_state(user_id=message.from_user.id, state=UserState.title_type_state)


@bot.message_handler(state=UserState.title_type_state)
def handle_movie_filter_type(message: Message) -> None:
    """
    Обрабатывает выбор типа (фильм/сериал) пользователем.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return

    with bot.retrieve_data(message.from_user.id) as data:
        if message.text.strip() == 'фильм':
            data['type'] = 'movie'
        elif message.text.strip() == 'сериал':
            data['type'] = 'tv-series'
        else:
            bot.send_message(message.chat.id, "Неверное значение, попробуйте ещё раз")
            return
    bot.reply_to(message, "Выберите год", reply_markup=reply_buttons('years'))
    bot.set_state(user_id=message.from_user.id, state=UserState.year_state)


@bot.message_handler(state=UserState.year_state)
def handle_movie_filter_year(message: Message) -> None:
    """
    Обрабатывает выбор года.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return
    with bot.retrieve_data(message.from_user.id) as data:
        data['year'] = message.text.strip()
    bot.reply_to(message, "Выберите жанр", reply_markup=reply_buttons('genres'))
    bot.set_state(user_id=message.from_user.id, state=UserState.genre_state)


@bot.message_handler(state=UserState.genre_state)
def handle_movie_filter_genre(message: Message) -> None:
    """
    Обрабатывает выбор жанра.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text.strip().lower()
    bot.reply_to(message, "Выберите рейтинг", reply_markup=reply_buttons('ratings'))
    bot.set_state(user_id=message.from_user.id, state=UserState.rate_state)


@bot.message_handler(state=UserState.rate_state)
def handle_movie_filter_rate(message: Message) -> None:
    """
    Обрабатывает выбор рейтинга.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return
    with bot.retrieve_data(message.from_user.id) as data:
        data['rate'] = message.text.strip()
    bot.reply_to(message, "Выберите максимальное количество результатов", reply_markup=reply_buttons('numbers'))
    bot.set_state(user_id=message.from_user.id, state=UserState.movie_limit_filter_state)


@bot.message_handler(state=UserState.movie_limit_filter_state)
def handle_movie_filter_limit(message: Message) -> None:
    """
    Обрабатывает выбор лимита результатов и выполняет поиск фильмов.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return

    with bot.retrieve_data(message.from_user.id) as data:
        t_type = data['type']
        t_year = data['year']
        t_genre = data['genre']
        t_rate = data['rate']

    try:
        limit = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте ещё раз")
        return
    else:
        bot.send_message(message.chat.id, "Идет поиск...", reply_markup=ReplyKeyboardRemove())

    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
    title_data = get_title_list(t_type=t_type, year=t_year, genre=t_genre, rate=t_rate, limit=limit)

    if len(title_data) > 0:
        with bot.retrieve_data(message.from_user.id) as data:
            data['search_result'] = title_data
        for index, title in enumerate(title_data):
            try:
                poster_url = title['poster']
                caption = formatters.format_movie_message(title)
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=poster_url,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=add_favorite_markup(index)
                )
            except (IndexError, KeyError) as exc:
                print(exc)
                bot.reply_to(message, 'Произошла ошибка, попробуйте ещё раз')
    else:
        bot.reply_to(message, "По вашему запросу ничего не найдено. Попробуйте другие фильтры.")

