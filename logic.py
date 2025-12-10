import json
import os


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

def mark_watched(movies: list[dict], movie_id: int) -> list[dict]:
    for movie in movies:
        if movie.get("id") == movie_id:
            movie["watched"] = True


    return movies

def find_by_year(movies: list[dict], year: int) -> list[dict]:
    # for movie in movies:
    #     if movie.get('year') == year:
    #         return movies
    return [movie for movie in movies if movie.get("year") == year]