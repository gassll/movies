from logic import load_movies, add_movie, save_movies, mark_watched, find_by_year

DATA_FILE = "movies.json"

def main():
    movies = load_movies(DATA_FILE)

    while True:
        print("\nКаталог фильмов")
        print("1. Показать все фильмы")
        print("2. Добавить фильм")
        print("3. Отметить фильм как просмотренный")
        print("4. Найти фильмы по году")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            if not movies:
                print("Список фильмов пуст.")
            else:
                print("\nСписок фильмов:")
                for movie in movies:
                    status = "Просмотрен" if movie["watched"] else "Не просмотрен"
                    print(f"[{movie['id']}] {movie['title']} ({movie['year']}) — {status}")
        elif choice == "2":
            title = input("Введите название фильма: ").strip()
            year_raw = input("Введите год: ").strip()

            if not year_raw.isdigit():
                print("Ошибка: год должен быть числом.")
                continue

            year = int(year_raw)

            add_movie(movies, title, year)
            save_movies(DATA_FILE, movies)

            print("Фильм успешно добавлен!")

        elif choice == "3":
            movie_id_raw = input("Введите ID фильма: ").strip()

            if not movie_id_raw.isdigit():
                print("Ошибка: ID должен быть числом.")
                continue

            movie_id = int(movie_id_raw)

            exists = any(movie.get("id") == movie_id for movie in movies)
            if not exists:
                print("Фильм с таким ID не найден.")
                continue

            mark_watched(movies, movie_id)
            save_movies(DATA_FILE, movies)
            print("Фильм отмечен как просмотренный!")

        elif choice == "4":
            year_raw = input("Введите год для поиска: ").strip()

            if not year_raw.isdigit():
                print("Ошибка: год должен быть числом.")
                continue

            year = int(year_raw)
            results = find_by_year(movies, year)

            if not results:
                print(f"Фильмов за {year} год не найдено.")
            else:
                print(f"Фильмы за {year} год:")
                for movie in results:
                    status = "Просмотрен" if movie["watched"] else "Не просмотрен"
                    print(f"[{movie['id']}] {movie['title']} ({movie['year']}) — {status}")

        elif choice == "0":
            save_movies(DATA_FILE, movies)
            print("До свидания!")
            break

        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()