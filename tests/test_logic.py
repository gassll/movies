import json
import os
from typing import List, Dict

import pytest

from logic import (
    load_movies,
    save_movies,
    add_movie,
    mark_watched,
    find_by_year,
)


# ---------- Фикстуры ----------

@pytest.fixture
def sample_movies() -> List[Dict]:
    """Базовый список фильмов для тестов."""
    return [
        {"id": 1, "title": "The Matrix", "year": 1999, "watched": False},
        {"id": 2, "title": "Inception", "year": 2010, "watched": True},
        {"id": 3, "title": "Interstellar", "year": 2014, "watched": False},
    ]


# ---------- Тесты для load_movies ----------

def test_load_movies_returns_empty_list_if_file_not_exists(tmp_path):
    path = tmp_path / "no_such_file.json"
    movies = load_movies(str(path))
    assert movies == []


def test_load_movies_reads_valid_json(tmp_path):
    path = tmp_path / "movies.json"
    data = [
        {"id": 1, "title": "Test", "year": 2000, "watched": False},
        {"id": 2, "title": "Test 2", "year": 2001, "watched": True},
    ]
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    movies = load_movies(str(path))

    assert isinstance(movies, list)
    assert len(movies) == 2
    assert movies[0]["title"] == "Test"
    assert movies[1]["watched"] is True


def test_load_movies_invalid_json_returns_empty_list(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{ это не валидный json", encoding="utf-8")

    movies = load_movies(str(path))

    assert movies == []


# ---------- Тесты для save_movies ----------

def test_save_movies_writes_valid_json(tmp_path, sample_movies):
    path = tmp_path / "movies.json"

    save_movies(str(path), sample_movies)

    assert path.exists()

    content = path.read_text(encoding="utf-8")
    loaded = json.loads(content)

    assert isinstance(loaded, list)
    assert len(loaded) == len(sample_movies)
    assert loaded[0]["title"] == "The Matrix"
    assert loaded[1]["watched"] is True


# ---------- Тесты для add_movie ----------

def test_add_movie_to_empty_list():
    movies: List[Dict] = []

    updated = add_movie(movies, "New Film", 2024)

    assert len(updated) == 1
    movie = updated[0]
    assert movie["id"] == 1
    assert movie["title"] == "New Film"
    assert movie["year"] == 2024
    assert movie["watched"] is False


def test_add_movie_increments_id(sample_movies):
    updated = add_movie(sample_movies, "Another Film", 2024)

    assert len(updated) == 4
    new_movie = updated[-1]
    assert new_movie["id"] == 4   # max id (3) + 1
    assert new_movie["title"] == "Another Film"
    assert new_movie["watched"] is False


# ---------- Тесты для mark_watched ----------

def test_mark_watched_sets_flag_true(sample_movies):
    updated = mark_watched(sample_movies, 1)

    movie = next(m for m in updated if m["id"] == 1)
    assert movie["watched"] is True


def test_mark_watched_does_not_fail_if_id_not_found(sample_movies):
    before = [m.copy() for m in sample_movies]

    updated = mark_watched(sample_movies, 999)

    # список не должен измениться
    assert updated == before


# ---------- Тесты для find_by_year ----------

def test_find_by_year_returns_matching_movies(sample_movies):
    result = find_by_year(sample_movies, 2010)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "Inception"


def test_find_by_year_returns_empty_list_if_no_matches(sample_movies):
    result = find_by_year(sample_movies, 1900)

    assert result == []


def test_find_by_year_does_not_modify_original_list(sample_movies):
    before = [m.copy() for m in sample_movies]

    _ = find_by_year(sample_movies, 2010)

    assert sample_movies == before