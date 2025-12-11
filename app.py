from logic import load_movies, add_movie, save_movies, mark_watched, find_by_year, action_find_by_year, \
    action_mark_watched, action_add_movie, action_load_movies

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
            action_load_movies(movies)
        elif choice == "2":
            action_add_movie(movies)
        elif choice == "3":
            action_mark_watched(movies)
        elif choice == "4":
            action_find_by_year(movies)
        elif choice == "0":
            save_movies(DATA_FILE, movies)
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()