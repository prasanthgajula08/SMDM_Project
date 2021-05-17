# SMDM_Project
* This website allows users to know the review of a movie based on the sentiment of people on twitter platform
* Code is available at https://github.com/prasanthgajula08/SMDM_Project

## Setup (Includes version requirements and instructions to install)
* python (version 3.9.1 or above) 
  ```
  Dowload from this link https://www.python.org/downloads/
  ```
* pip (version 21..1.1 or above)
* django (version 2.1.1 or above) 
  ```
  $pip install django
  ```
* requests (version 2.25.1 or above) 
  ```
  $pip install requests
  ```
* pandas (version 1.2.4 or above) 
  ```
  $pip install pandas
  ```
* Git (version 2.26.0.windows.1 or above)
  ```
  Download from this link https://git-scm.com/download/win
  ```
* snscrape (version 0.3.5.dev104+g97c8cae or above) 
  ```
  $pip install git+https://github.com/JustAnotherArchivist/snscrape.git
  ```
* nltk (version 3.6.2 or above) 
  ```
  $pip install nltk
  ```
* pycountry (version 20.7.3 or above) 
  ```
  $pip install pycountry
  ```
  
## Instructions to run
* Move to Twitter_Review directory
  ```
  cd Twitter_Review
  ```
* Enter this command
  ```
  python manage.py runserver
  ```
* Open browser and go to local host "127.0.0.1:8000"
* Now go to "reelgood.com" on other tab and search for the movie that you want review for.
* Select the movie that you searched for and then copy the string taht is after reelgood.com/ which is present in the url.
* Come back to local host tab and paste that string in the search box of our website and hit search.

## Notes
* The number of tweets on which the website is gonna perform sentiment analysis is set to 100000 by default.
* To change that number you need to manually go to SMDM_Project/Twitter_Review/WebScraper/views.py and replace the number 100000 (on line numbers 126 and 147) with whatever number you wish to perform analysis on.
* All the setup instructions are for windows operating system.
* For better viewing experience of the webpage set scale to 100% in your system display settings.

## Runtime
* For 100000 tweets collected it takes approximately 18 mins
* For 5000 tweets collected it takes approximately 1 min
