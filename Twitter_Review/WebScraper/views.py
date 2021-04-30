from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import requests
import bs4
# Create your views here.


def home(request):
    return render(request, 'home.html')


def fetchData(request):
    movie = Movie()
    searchedValue = request.POST['searchValue']

    url = "https://www.reelgood.com/movie/" + searchedValue
    html_code = requests.get(url)
    bs_code = bs4.BeautifulSoup(html_code.text, 'lxml')

    title = searchedValue
    movie.title = title

    images = bs_code.find_all("img", {"class": "css-1sz776d e1181ybh1"})
    image = images[2]['src']
    with open('static/images/pic1.jpg', 'wb') as handle:
        response = requests.get(image, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    imdb_rating = bs_code.find_all(
        "span", {"class": "css-xmin1q ey4ir3j3"})[0].getText()
    movie.imdb = imdb_rating

    if float(imdb_rating) > 0 and float(imdb_rating) <= 5:
        movie.won = "Hell No!"
    elif float(imdb_rating) > 5 and float(imdb_rating) <= 8:
        movie.won = "May be ¯\_(ツ)_/¯"
    else:
        movie.won = "Definitely recommended!"

    description = bs_code.find_all(
        "p", {"itemprop": "description"})[0].getText()
    movie.desc = description

    genre = bs_code.find_all("a", {"class": "css-10wrqt0"})[0].getText()
    movie.genre = genre

    cnc = bs_code.find_all("h3", {"class": "css-i6ptp9 egg5eqo2"})
    lis = []
    for i in cnc:
        lis.append(i.getText())
    movie.cnc = lis

    wtw = bs_code.find_all("title")[0].getText()
    if "Where to Watch It" in wtw:
        movie.wtw = "NA"
    else:
        start = wtw.index("Watch on")
        end = wtw.index("|")
        movie.wtw = wtw[start:end]
    
    trailer = bs_code.find_all("a", {"class": "css-zniopz e14injhv8"})
    if len(trailer)>0:
        movie.trailer = trailer[0]['href']
    else:
        movie.trailer = "NA"

    return render(request, 'info.html', {'movie': movie})
