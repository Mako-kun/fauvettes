from bs4 import BeautifulSoup

from datetime import date
import requests
import json
import sys, getopt

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "ov", ["help", "output", "verbose"])
except getopt.GetoptError:
    print (sys.argv[0] + " -os --output --silent")
    sys.exit(1)

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

output = silent = False

r = requests.get(baseSite)
soup = BeautifulSoup(r.text, 'html.parser')
for d in soup.find(class_="menu-seance").find_all('li'):
    dates.append(d["data-date-sql"])

for opt in opts:
    if (opt in ("-o", "--output")):
        output = True;
    elif (opt in ("-s", "--silent")):
        silent = True;

currentDate = date.today().strftime("%Y-%m-%d")
file = open("events-"+currentDate+".txt", "w")

for indexFilm, film in enumerate(programmation):
    outputStr = "Séances pour \""+film+"\" :\n"
        
    if (ids[indexFilm]):
        for indexDate, date in enumerate(dates):
            r = requests.post(baseSite+"index.php?do=ajax/fetchSeancesByDayAndFilm", {"filmId":str(ids[indexFilm]), "date":dates[indexDate]})
            movieDict = json.loads(r.text)
            seances = movieDict["progs"]
            if (seances):
                for seance in seances:
                    outputStr += date+" @ "+seance['heureDebut']+" ("+seance["version"]+")\n"
                    if file:
                        file.write(date+" "+seance['heureDebut']+" ; "+film+" ; "+"Les Fauvettes ; "+seance["version"]+"\n")
    
    if not silent:
        print (outputStr)
        
if output:
    file.close()