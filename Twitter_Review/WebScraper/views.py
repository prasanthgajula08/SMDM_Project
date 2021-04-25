from django.shortcuts import render
from django.http import HttpResponse
import requests
import bs4
# Create your views here.

def home(request):
    return render(request, 'home.html')

def fetchData(request):
    searchedValue = request.POST['searchValue']
    url = "https://www.google.com/search?q=" + searchedValue
    html_code = requests.get(url)
    bs_code = bs4.BeautifulSoup(html_code.text, 'lxml')
    title = bs_code.select('title')[0].getText()
    return render(request, 'info.html', {'title':title})