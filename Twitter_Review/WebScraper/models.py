from django.db import models

# Create your models here.

class Movie:
    title: str
    imdb: float
    desc: str
    genre: str
    cnc: list
    wtw: str
    won: str
    trailer: str
    tweets: list
    sentiments: list
    sent_val: float
    review: str
    locations: list