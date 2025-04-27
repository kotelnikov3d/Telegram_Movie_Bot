from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from telebot.handler_backends import State, StatesGroup
from telebot.custom_filters import StateFilter
from typing import Dict


# Инициализация памяти для состояний
storage = StateMemoryStorage()
# Инициализация бота
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
bot.add_custom_filter(StateFilter(bot))


# Определение состояний
class UserState(StatesGroup):
    """
    Класс для определения состояний пользователя в процессе взаимодействия с ботом.
    """
    name_state = State()  # Состояние для ввода имени
    title_type_state = State()  # Состояние для выбора типа (фильм, сериал)
    year_state = State()  # Состояние для выбора года
    genre_state = State()  # Состояние для выбора жанра
    rate_state = State()  # Состояние для выбора рейтинга
    movie_limit_search_state = State()  # Состояние для выбора максимального количества результатов
    movie_limit_filter_state = State()  # Состояние для выбора максимального количества результатов
    idle_state = State()
