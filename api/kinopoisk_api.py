import requests
from config_data.config import KP_API_KEY

# Базовый URL API Кинопоиска
BASE_URL = "https://api.kinopoisk.dev/"

# Заголовки запроса, включающие API-ключ
HEADERS = {
    "accept": "application/json",
    "X-API-KEY": KP_API_KEY
}


def parse_response(row_data: dict) -> list:
    """
    Разбирает JSON-ответ от API и формирует список с информацией о фильмах.

    :param row_data: Словарь с JSON-данными, полученными от API.
    :return: Список словарей с данными о фильмах.
    """
    title_list = []
    try:
        # Проверяем, содержит ли ответ список "docs"
        row_data_list = row_data.get('docs', [row_data])

        for title in row_data_list:
            title_info = {
                'name': title['name'],  # Название фильма
                'year': title['year'],  # Год выпуска
                'rating': f"KP: {title['rating']['kp']} IMDB: {title['rating']['imdb']}",  # Рейтинги KP и IMDB
                'genres': ', '.join([genre['name'] for genre in title['genres']]),  # Жанры
                'description': title.get('description', 'Описание отсутствует'),  # Описание
                'poster': title['poster']['url'],  # Ссылка на постер
                'countries': ', '.join([country['name'] for country in title['countries']]),  # Страны производства
                'type': title['type']  # Тип (фильм, сериал и т. д.)
            }
            title_list.append(title_info)
    except (IndexError, KeyError) as exc:
        print(f"Ошибка при разборе ответа API: {exc}")

    print(title_list)
    return title_list


def get_title_list(
        name: str = None,
        t_type: str = None,  # movie/tv-series
        year: str = None,  # 1874, 2050, !2020, 2020-2024
        genre: str = None,  # "драма", "комедия", "!мелодрама", "+ужасы"
        rate: str = "5-10",  # 7, 10, 7.2-10
        page: int = 1,
        limit: int = 5
) -> list:
    """
    Выполняет поиск фильмов на Кинопоиске по заданным параметрам.

    :param name: Название фильма (если известно).
    :param t_type: Тип (movie или tv-series).
    :param year: Год выпуска или диапазон лет.
    :param genre: Жанр или исключаемый жанр.
    :param rate: Рейтинг (KP) или его диапазон.
    :param page: Номер страницы результатов.
    :param limit: Количество элементов на странице.
    :return: Список фильмов, соответствующих параметрам поиска.
    """
    # Определяем конечную точку API
    if not name and not year:
        endpoint = "movie/random"
    elif name and not year:
        endpoint = "movie/search"
    else:
        endpoint = "movie"

    url = f"{BASE_URL}v1.4/{endpoint}"

    # Формируем параметры запроса
    params = {
        'page': page,
        'limit': limit,
        'query': name,
        'type': t_type,
        'year': year,
        'genres.name': genre,
        'rating.kp': rate
    }

    # Удаляем параметры с None-значением
    params = {k: v for k, v in params.items() if v is not None}

    print(f'Запрос с параметрами: {params}')
    print(f'Используемый endpoint: {endpoint}')

    # Выполняем запрос к API
    response = requests.get(url, headers=HEADERS, params=params)
    json_resp = response.json()

    print('Ответ сервера:')
    print(json_resp)

    return parse_response(json_resp)
