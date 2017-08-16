import webbrowser


class Movie():

    """
    The movie class which contains movie information
    (title, storyline, poster_image, youtube_url)
    """

    def __init__(self, movie_title, movie_storyline,
                 poster_image, trailer_youtube):
        """
        initialize the attributes of the class
        """
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        """
        open the correspond web page of trailer_youtube_url
        """
        webbrowser.open(self.trailer_youtube_url)

