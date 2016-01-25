from bs4 import BeautifulSoup
from datetime import date

import time
import requests
import json

class Salle:    
    def __init__(self, idS, num):
        self.id = idS
        self.num = num
        self.seances = []

class Film:
    def __init__(self, idDist, title, link):
        self.idDist = idDist
        self.title = title
        self.link = link
        self.seances = []
        
    def __str__(self):
        return self.title
        
    __repr__ = __str__

today = date.today()

salles = [
    Salle(7330, 1),
    Salle(7324, 2),
    Salle(7328, 3),
    Salle(7326, 4),
    Salle(7332, 5)
]

dates = []
films = []

baseSite = "http://www.cinemalesfauvettes.com/"

r = requests.get(baseSite)
soup = BeautifulSoup(r.text, 'html.parser')
for date in soup.find(class_="menu-seance").find_all('li'):
    dates.append(date["data-date-sql"])

r = requests.get(baseSite+"?do=ajax/fetchMenuFilms")
soup = BeautifulSoup(r.text, "html.parser")

for idx, filmDiv in enumerate(soup.find_all("li"), start=0):
    if (idx == 0):
        continue
    
    link = filmDiv.a["href"]
    title = filmDiv.find(class_="libelle-small").string
    
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    idDist = None
    try:
        if (soup.find(id="seance-film")):
            idDist = soup.find(id="seance-film").find("ul", class_="les-jours")["data-film-id"]
    except:
        pass

    contentDiv = soup.find(class_="film-content")

    films.append(Film(
        idDist,
        title,
        link
    ))

filmsDiff = []
for film in films:
    if (film.idDist != None):
        filmsDiff.append(film)
    
filmsNext = list(set(films) - set(filmsDiff))
filmsNext = sorted(filmsNext, key=lambda x: x.title)

print("Liste des films diffusés :")
print("==========================")

gen = (x for x in filmsDiff if x.idDist != None)
for idx, film in enumerate(gen, start=0):
    print(str(idx)+") "+film.title)

choice = input("\nChoisissez votre film : ")

for idx, date in enumerate(dates, start=0):
    print("#"+str(idx)+" "+date)

choiceDate = input("\nChoisissez une date : ")

strTitle = "\nListe des séances pour "+filmsDiff[int(choice)].title+" ("+dates[int(choiceDate)]+")"
print(strTitle)
print("="*len(strTitle))

try:    
    r = requests.post(baseSite+"index.php?do=ajax/fetchSeancesByDayAndFilm", {"filmId":filmsDiff[int(choice)].idDist, "date":dates[int(choiceDate)]})
    soup = BeautifulSoup(r.text, "html.parser")
    movieDict = json.loads(str(soup))
        
    for seance in movieDict["progs"]:
        films[0].seances.append(seance)

    for seance in films[0].seances:
        print (seance["heureDebut"]+" ("+seance["version"]+")", end=" | ")
except:
    print ("Une erreur s'est produite.")