from bs4 import BeautifulSoup
from datetime import date

import time
import requests
import json

dates = []
programmation = ['ARRIETTY, LE PETIT MONDE DES CHAPARDEURS',
 'LA COLLINE AUX COQUELICOTS',
 'LES CONTES DE TERREMER',
 'LE CHÂTEAU AMBULANT',
 'LE VENT SE LEVE',
 'LE VOYAGE DE CHIHIRO',
 'PONYO SUR LA FALAISE',
 'PORCO ROSSO',
 'PRINCESSE MONONOKE',
 'LE ROYAUME DES CHATS',
 'MES VOISINS LES YAMADA',
 'MON VOISIN TOTORO']

ids = [5312, 6609, 2656, 716, 9868, 515, 3805, 11868, 583, 246, None, 731]

baseSite = "http://www.cinemalesfauvettes.com/"

r = requests.get(baseSite)
soup = BeautifulSoup(r.text, 'html.parser')
for date in soup.find(class_="menu-seance").find_all('li'):
    dates.append(date["data-date-sql"])

for indexFilm, film in enumerate(programmation):
    # print ("Séances pour \""+film+"\" :")
    if (ids[indexFilm]):
        for indexDate, date in enumerate(dates):
            r = requests.post(baseSite+"index.php?do=ajax/fetchSeancesByDayAndFilm", {"filmId":str(ids[indexFilm]), "date":dates[indexDate]})
            movieDict = json.loads(r.text)
            seances = movieDict["progs"]
            if (seances):
                for seance in seances:
                    print (date+" "+seance['heureDebut']+" "+film+" ; "+"Les Fauvettes ; "+seance["version"])
    # else:
        # print ("Pas de séance pour ce film.\n")
    # print ("")