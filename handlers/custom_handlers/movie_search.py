from telebot.types import Message, ReplyKeyboardRemove
from loader import bot, UserState
from api.kinopoisk_api import get_title_list
from utils.misc import formatters
from keyboards.reply.reply_markup import reply_buttons
from keyboards.inline.inline_markup import add_favorite_markup


@bot.message_handler(commands=["movie_search"])
def handle_movie_search_by_name(message: Message) -> None:
    """
    Запускает процесс поиска фильмов по названию.
    """
    bot.reply_to(message, "Введите название фильма/сериала:")
    bot.set_state(user_id=message.from_user.id, state=UserState.name_state)


@bot.message_handler(state=UserState.name_state)
def handle_movie_name(message: Message) -> None:
    """
    Обрабатывает ввод названия фильма пользователем.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['name'] = message.text.strip()
    bot.reply_to(message, "Выберите максимальное количество результатов", reply_markup=reply_buttons('numbers'))
    bot.set_state(user_id=message.from_user.id, state=UserState.movie_limit_search_state)


@bot.message_handler(state=UserState.movie_limit_search_state)
def handle_movie_limit(message: Message) -> None:
    """
    Обрабатывает выбор лимита результатов и выполняет поиск фильмов по названию.
    """
    if '/' in message.text:
        bot.reply_to(message, "Попробуйте ещё раз или нажмите /exit чтобы выйти из поиска")
        return
    with bot.retrieve_data(message.from_user.id) as data:
        name = data['name']
        bot.send_message(message.chat.id, "Идет поиск...", reply_markup=ReplyKeyboardRemove())
        title_data = get_title_list(name=name, limit=int(message.text.strip()))
        data['search_result'] = title_data
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
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
