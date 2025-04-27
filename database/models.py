from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField
from config_data.config import DB_PATH

# Создаём подключение к базе данных

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """
    Базовая модель, от которой наследуются все остальные модели.
    """

    class Meta:
        database = db


# Модель пользователя
class User(BaseModel):
    """
    Модель для хранения информации о пользователях.
    """
    user_id = IntegerField(primary_key=True)  # Уникальный идентификатор пользователя
    first_name = CharField()  # Имя


# Модель фильма
class Movie(BaseModel):
    """
    Модель для хранения информации о фильмах.
    """
    movie_id = AutoField()  # Уникальный идентификатор фильма
    user = ForeignKeyField(User, backref="movies")  # Связь с пользователем
    name = CharField()  # Название фильма
    year = IntegerField()  # Год выпуска
    rating = CharField()  # Рейтинг
    genres = CharField()  # Жанры
    countries = CharField()  # Страны производства
    description = CharField()  # Описание
    poster = CharField()  # Ссылка на постер
    type = CharField()  # Тип (фильм, сериал и т. д.)

    def get_info(self) -> dict:
        """
        Возвращает информацию о фильме в виде словаря.

        :return: Словарь с информацией о фильме
        """
        title_info = {
            'name': self.name,
            'year': self.year,
            'rating': self.rating,
            'genres': self.genres,
            'description': self.description,
            'poster': self.poster,
            'countries': self.countries,
            'type': self.type
        }
        return title_info


def create_models():
    """
    Создаёт таблицы для всех моделей, унаследованных от BaseModel.
    """
    db.create_tables(BaseModel.__subclasses__())
