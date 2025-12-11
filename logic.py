import json
import os
DATA_FILE = "movies.json"

def action_load_movies(movies):
    if not movies:
        print("Список фильмов пуст.")
    else:
        print("\nСписок фильмов:")
        for movie in movies:
            status = "Просмотрен" if movie["watched"] else "Не просмотрен"
            print(f"[{movie['id']}] {movie['title']} ({movie['year']}) — {status}")

def load_movies(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return []

    if isinstance(data, list):
        return data
    return []


def save_movies(path: str, movies: list[dict]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)


def action_add_movie(movies: list[dict]) -> None:
    title = input("Введите название фильма: ").strip()
    year_raw = input("Введите год: ").strip()

    if not year_raw.isdigit():
        print("Ошибка: год должен быть числом.")
        return

    year = int(year_raw)

    add_movie(movies, title, year)
    save_movies(DATA_FILE, movies)

    print("Фильм успешно добавлен!")

def add_movie(movies: list[dict], title: str, year: int) -> list[dict]:
    if movies:
        max_id = max(movie.get('id', 0) for movie in movies)
    else:
        max_id = 0

    new_movie = {
        'id': max_id + 1,
        'title': title,
        'year': year,
        'watched': False
    }

    movies.append(new_movie)
    return movies

def action_mark_watched(movies: list[dict]) -> list[dict]:
    movie_id_raw = input("Введите ID фильма: ").strip()

    if not movie_id_raw.isdigit():
        print("Ошибка: ID должен быть числом.")
        return

    movie_id = int(movie_id_raw)

    exists = any(movie.get("id") == movie_id for movie in movies)
    if not exists:
        print("Фильм с таким ID не найден.")
        return

    mark_watched(movies, movie_id)
    save_movies(DATA_FILE, movies)
    print("Фильм отмечен как просмотренный!")

def mark_watched(movies: list[dict], movie_id: int) -> list[dict]:
    for movie in movies:
        if movie.get("id") == movie_id:
            movie["watched"] = True
            break

    return movies

def action_find_by_year(movies: list[dict]) -> list[dict]:
        year_raw = input("Введите год для поиска: ").strip()

        if not year_raw.isdigit():
            print("Ошибка: год должен быть числом.")
            return

        year = int(year_raw)
        results = find_by_year(movies, year)

        if not results:
            print(f"Фильмов за {year} год не найдено.")
        else:
            print(f"Фильмы за {year} год:")
            for movie in results:
                status = "Просмотрен" if movie["watched"] else "Не просмотрен"
                print(f"[{movie['id']}] {movie['title']} ({movie['year']}) — {status}")


def find_by_year(movies: list[dict], year: int) -> list[dict]:
    return [movie for movie in movies if movie.get("year") == year]