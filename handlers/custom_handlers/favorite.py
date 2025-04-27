from telebot.types import Message, CallbackQuery
from loader import bot, UserState
from utils.misc import formatters
from database.models import Movie, User
from keyboards.inline.inline_markup import add_movies_buttons
from config_data.config import FAVORITE_PAGE_SIZE


def show_favorite(chat_id: int, movies_data, page) -> None:
    """
    Отображает список избранных фильмов пользователя.

    :param chat_id: Идентификатор чата, в который отправляется сообщение.
    :param movies_data: Список избранных фильмов.
    :param page: Текущая страница.
    :return: None
    """

    page_size = FAVORITE_PAGE_SIZE
    f_movie = 0 + (page_size * page)
    l_movie = f_movie + page_size
    l_page = len(movies_data) // (FAVORITE_PAGE_SIZE + 0.1)
    print('l_page', l_page)

    try:
        text = formatters.format_favorite_list_message(movies_data[f_movie:l_movie])
        bot.send_message(chat_id, text,
                         reply_markup=add_movies_buttons(movies_data[f_movie:l_movie], page, l_page))
    except (IndexError, KeyError) as exc:
        print(exc)
        bot.send_message(chat_id, 'Произошла ошибка, попробуйте ещё раз')


@bot.callback_query_handler(func=lambda call: True)
def handle_movie_add_favorite(call: CallbackQuery) -> None:
    """
    Обрабатывает нажатия на инлайн-кнопки:
    - Добавление фильма в избранное.
    - Показ информации о фильме.
    - Переключение страниц избранного.

    :param call: Объект CallbackQuery, содержащий данные о нажатой кнопке.
    :return: None
    """
    if 'add_favorite' in call.data:
        index = int(call.data.split('_')[-1])
        with bot.retrieve_data(call.from_user.id) as data:
            print(data)
            movie_data = data['search_result'][index]
            movie_data['user_id'] = call.from_user.id

        try:
            favorite_movie = Movie(**movie_data)
            favorite_movie.save()
            bot.send_message(call.message.chat.id, 'Фильм успешно добавлен в избранное')
        except (IndexError, KeyError) as exc:
            print(exc)
            bot.send_message(call.message.chat.id, 'Произошла ошибка, попробуйте ещё раз')

    elif 'show_movie' in call.data:
        with bot.retrieve_data(call.from_user.id) as data:
            page = data.get('page', 0)
            index = int(call.data.split('_')[-1]) + (FAVORITE_PAGE_SIZE * page)
            print('index', index)
            movies_data = data['favorite_list']

        try:
            with bot.retrieve_data(call.from_user.id) as data:
                if 'last_message_id' in data:
                    bot.delete_message(call.message.chat.id, data['last_message_id'])

                poster_url = movies_data[index]['poster']
                caption = formatters.format_movie_message(movies_data[index])
                msg_data = bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=poster_url,
                    caption=caption,
                    parse_mode="Markdown"
                )
                print('id - ', msg_data.message_id)
                data['last_message_id'] = msg_data.message_id
        except (IndexError, KeyError) as exc:
            print(exc)
            bot.send_message(call.message.chat.id, 'Произошла ошибка, попробуйте ещё раз')

    elif 'favorite_next_page' in call.data:
        bot.delete_message(call.message.chat.id, call.message.id)
        with bot.retrieve_data(call.from_user.id) as data:
            data['page'] = data.get('page', 0) + 1
            show_favorite(call.message.chat.id, data['favorite_list'], data['page'])

    elif 'favorite_back_page' in call.data:
        bot.delete_message(call.message.chat.id, call.message.id)
        with bot.retrieve_data(call.from_user.id) as data:
            data['page'] = data.get('page', 0) - 1
            show_favorite(call.message.chat.id, data['favorite_list'], data['page'])


@bot.message_handler(commands=["favorite"])
def handle_view_favorite(message: Message) -> None:
    """
    Обрабатывает команду /favorite, отображая список избранных фильмов пользователя.

    :param message: Объект Message, содержащий информацию о сообщении и пользователе.
    :return: None
    """
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
    user = User.get_or_none(User.user_id == message.from_user.id)

    if not user:
        bot.send_message(message.chat.id, 'Здесь пока ничего нет, добавьте какой-нибудь фильм')
        return

    # if message.from_user.id not in user_data:
    #     print('Добавляем пользователя в словарь')
    with bot.retrieve_data(message.from_user.id) as data:
        data['page'] = 0
        movies = user.movies
        movies_data = list(reversed([movie.get_info() for movie in movies]))
        if len(movies_data) == 0:
            bot.send_message(message.chat.id, 'Здесь пока ничего нет, добавьте какой-нибудь фильм')
            return
        data['favorite_list'] = movies_data
        show_favorite(message.chat.id, movies_data, page=0)
