from django.shortcuts import render
from django.http import HttpResponse
import requests
import bs4
# Create your views here.

def home(request):
    return render(request, 'home.html')

def fetchData(request):
    searchedValue = request.POST['searchValue']
    #url = "https://www.google.com/search?q=" + searchedValue
    url = "https://www.reelgood.com/movie/" + searchedValue
    html_code = requests.get(url)
    bs_code = bs4.BeautifulSoup(html_code.text)
    title = bs_code.select('title')[0].getText()

    images = bs_code.find_all("img", {"class": "css-1sz776d e1181ybh1"})
    image = images[2]['src']
    
    return render(request, 'info.html', {'title':title}, {'image':image})