import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KP_API_KEY = os.getenv("KP_API_KEY")
DB_PATH = "database\\my_database.db"
FAVORITE_PAGE_SIZE = 12
DEFAULT_COMMANDS = (
    ("start", "🚀Запустить бота"),
    ("random_movie", "🎲Случайный фильм"),
    ("random_series", "📺Случайный сериал"),
    ("movie_search", "🔍Фильм/сериал по названию"),
    ("movie_by_filter", "🎭Фильм/сериал по фильтрам"),
    ("favorite", "📜Избранное"),
    ("help", "❓Справка")
)
