from bs4 import BeautifulSoup
from datetime import date

import time
import requests
import json

dates = []
films = []

baseSite = "http://www.cinemalesfauvettes.com/"

r = requests.get(baseSite)
soup = BeautifulSoup(r.text, 'html.parser')
for date in soup.find(class_="menu-seance").find_all('li'):
    # print (time.strptime(date["data-date-sql"], "%Y-%m-%d"))
    dates.append(time.strptime(date["data-date-sql"], "%Y-%m-%d"))
    
# for date in dates:
#     print (time.strftime("%Y-%m-%d", date))
    
r = requests.get(baseSite+"index.php?do=ajax/fetchMoreFilmsCycle&start=0&limit=15&cycle-id=16")
soup = BeautifulSoup(r.text, "html.parser")

# print(r.text)
print(json.load(r))

# print(movieDict)

# for idx, filmDiv in enumerate(soup["html"].find_all(class_="content-b")):
    # link = filmDiv.a["href"]
    # title = filmDiv.find(class_="libelle-small").string
    # print (link)

# for idx, filmDiv in enumerate(soup.find_all("li"), start=0):
#     if (idx == 0):
#         continue
#
#     link = filmDiv.a["href"]
#     title = filmDiv.find(class_="libelle-small").string
#
#     r = requests.get(link)
#     soup = BeautifulSoup(r.text, "html.parser")
#
#     idDist = None
#     try:
#         if (soup.find(id="seance-film")):
#             idDist = soup.find(id="seance-film").find("ul", class_="les-jours")["data-film-id"]
#     except:
#         pass
#
#     contentDiv = soup.find(class_="film-content")
#
#     films.append(Film(
#         idDist,
#         title,
#         link
#     ))
#
# filmsDiff = []
# for film in films:
#     if (film.idDist != None):
#         filmsDiff.append(film)
#
# filmsNext = list(set(films) - set(filmsDiff))
# filmsNext = sorted(filmsNext, key=lambda x: x.title)