# coding: utf-8
import json
import codecs
from datetime import datetime


def getdate(line):
    """ get a clean string and try to return a date """
    #s = "2016-03-26T09:25:55.000Z"
    #f = "%Y-%m-%dT%H:%M:%S.%fZ"
    dateformat1 = "%d %m %Y"
    dateformat2 = "%d %m"
    try:
        res = datetime.strptime(line, dateformat1)
#        print(res)
        return res
    except ValueError:
        res = datetime.strptime(line, dateformat2)
#        print(res)
        return res


REP = ["cour 6", "cour 9", "cour 7", "cour 10", "(", ")",
       "place", "avenue", "rue", "boulevard", "impasse", "square", "rond-point", "quai", "plaça",
       "carrefour", "allées", "allée", "promenade", "trocadéro", "lotissement", "chemin", "passage",
       "esplanade", "parc", "pont", "voie", "de la pce", "passerelle", "passe", "rond point",
       "rampe", "faubourg", "traverse",
       "du ", " et ", "des", "de ", "la ", "le ",
       "libération", "(alias", "route", "ex  roderneweg", "reignat", "boisséjour",
       "dom sncf", "cours", "bis", "souvenir franc", "privée",
       "victimes", "légion d'honneur", "25 fusillés", "déportés", "fusillés", "plaine",
       "grand", "petit", "nuit", "martyrs", "combats", "bombardement", "crech",
       "l'appel", "lcie", "victoire", "plan", "rassemblement", "Indulto", "dunlop"
       ]
REPDAY = {"1Er": "01", "1er": "01", "premier": "01",
          "onze":"11", "douze": "12", "treize":"13", "quatorze": "14", "quinze":"15", 
          "seize":"16", "dix sept": "17", "dix huit": "18", "dix neuf": "19",
          "vingt-":"2", "vingt":"20", "trente-":"3", "trente":"30",
          "un": "1", "deux":"2", "trois": "3", "quatre":"4", "cinq":"5", "six":"6", "sept":"7",
          "huit":"8", "neuf":"9", "dix-":"1", "dix":"10"}
REPMONTH = {"janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05",
            "juin": "06", "juillet": "07", "août": "08", "septembre": "09",
            "octobre": "10", "novembre": "11", "décembre": "12"}

def cleanstr(line):
    res = line.lower()
    for reps in REP:
        res = res.replace(reps, "")
    for torep, rep in REPMONTH.items():
        res = res.replace(torep, rep)
    for torep, rep in REPDAY.items():
        res = res.replace(torep, rep)
    res = res.strip()
    return res

def readfile(filename):
    """ clean all character which are not part of a date """
    jsonlines = json.load(codecs.open(filename, 'r', 'utf-8'))
    #print(jsonlines)
    for line in jsonlines:
        cleanedstr = cleanstr(line['name'])
        #print("{} --> |{}|".format(line['name'], cleanedstr))
        try:
            getdate(cleanedstr)
        except ValueError:
            print("Error on |{}| from {}".format(cleanedstr, line['name']))
        

if __name__ == "__main__":
    readfile("france.json")

