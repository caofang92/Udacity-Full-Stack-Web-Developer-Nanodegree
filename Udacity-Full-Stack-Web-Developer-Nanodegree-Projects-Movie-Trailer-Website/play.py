import fresh_tomatoes
import movie


# movie
Pikachu_song = movie.Movie(
        "Pikachu_song",
        "Pikachu_song",
        "https://cdn.gamerant.com/wp-content/uploads/Pokemon-Name-Change-Hong-Kong.jpg.optimal.jpg",  # noqa
        "https://www.youtube.com/watch?v=l8UxQ0DC2gs&list=PLPIQinjoPbI277S1eXPFXM9r6wfKWF7xw")        # noqa

kobe_video = movie.Movie(
        "kobe",
        "kobe career highlights",
        "https://cavypop.com/wp-content/uploads/2016/11/011216_kob.jpg",
        "https://www.youtube.com/watch?v=gIWZaGjwDNA")

caixingjuan_video = movie.Movie(
        "cai xingjuan",
        "My favorite chinese singer",
        "http://s2.buzzhand.net/uploads/08/2/997410/1479376271737.jpg",
        "https://www.youtube.com/watch?v=UYqnC9hKsCs&list=PLQdSA-hJXiMB7iXE3tW_CZspBVQ0HlGZK&index=17")  # noqa

# movie list
movies = [kobe_video, caixingjuan_video, Pikachu_song]

# generate and open a Movie Trailer Website based on the input movie list
fresh_tomatoes.open_movies_page(movies)

