# coding: utf-8
import json
import sys
import codecs
import re
from datetime import datetime
#import logging
#import logging.config

#logging.config.fileConfig('logging.conf')

#logger = logging.getLogger(__name__)
'''
impossibleparsing = ['{"name": "Place du 4 et 5 Septembre", "city": "Hargnies", "region": "Champagne-Ardenne", "country": "France", "lat": 50.019477, "lon": 4.790652}          , "dates": ["09_04", "09_05"]},',
                     '{"name": "Place du 11 Novembre et du 8 Mai", "city": "Essômes-sur-Marne", "region": "Picardie", "country": "France", "lat": 49.029142, "lon": 3.37383}    , "dates": ["11_11", "05_08"]},', 
                     '{"name": "Rue des 19 et 20 Juin 1907", "city": "Cuxac-d"Aude", "region": "Languedoc-Roussillon", "country": "France", "lat": 43.24415, "lon": 2.998209}   , "dates": ["06_19", "06_20"]},',
                     '{"name": "Rue des 14 et 15 Avril 1945", "city": "Vaux-sur-Mer", "region": "Poitou-Charentes", "country": "France", "lat": 45.646181, "lon": -1.060556}    , "dates": ["04_14", "04_15"]},',
                     '{"name": "Place du 11 Nov 1918 et 8 Mai 45", "city": "Autricourt", "region": "Bourgogne", "country": "France", "lat": 47.997219, "lon": 4.61962}          , "dates": ["11_11", "05_08"]},',
                     '{"name": "Rue des 9 et 10 Juin 1940", "city": "Venables", "region": "Haute-Normandie", "country": "France", "lat": 49.200421, "lon": 1.297545}            , "dates": ["06_09", "06_10"]},',
                     '{"name": "Rue d\'9 10 Juin 1940", "city": "Dreux", "region": "Centre", "country": "France", "lat": 48.734489, "lon": 1.368024}                            , "dates": ["06_09", "06_10"]},',
                     '{"name": "Place du 11 Novembre et du 8 Mai", "city": "Herbault", "region": "Centre", "country": "France", "lat": 47.6056, "lon": 1.142072}                , "dates": ["11_11", "05_08"]},',
                     '{"name": "Place du 24-25 Juillet 1944", "city": "Donges", "region": "Pays de la Loire", "country": "France", "lat": 47.330319, "lon": -2.077903}          , "dates": ["07_24", "07_25"]},',
                     '{"name": "Place des 8 et 11 Mai 1945", "city": "Saint-Nazaire", "region": "Pays de la Loire", "country": "France", "lat": 47.278412, "lon": -2.216284}    , "dates": ["05_11", "05_08"]},',
                     '{"name": "Avenue des 4, 8 et 9 Septembre", "city": "Le Portel", "region": "Nord-Pas-de-Calais", "country": "France", "lat": 50.70666, "lon": 1.57299}     , "dates": ["09_04", "09_08", "09_09"]},',
                     '{"name": "Rue du Souvenir : 11 Novembre - 8 Mai - 19 Mars", "city": "Germagny", "region": "Bourgogne", "country": "France", "lat": 46.672714, "lon": 4.604167}    , "dates": ["11_11", "05_08", "03_19"]}']
'''
impossibleparsingdict = {
    "03_19": {'done': False, 'streets' : [{"name": "Rue du Souvenir : 11 Novembre - 8 Mai - 19 Mars", "city": "Germagny", "region": "Bourgogne", "country": "France", "lat": 46.672714, "lon": 4.604167}]},
    "04_14": {'done': False, 'streets' : [{"name": "Rue des 14 et 15 Avril 1945", "city": "Vaux-sur-Mer", "region": "Poitou-Charentes", "country": "France", "lat": 45.646181, "lon": -1.060556}]},
    "04_15": {'done': False, 'streets' : [{"name": "Rue des 14 et 15 Avril 1945", "city": "Vaux-sur-Mer", "region": "Poitou-Charentes", "country": "France", "lat": 45.646181, "lon": -1.060556}]},
    "05_08": {'done': False, 'streets' : [{"name": "Place du 11 Novembre et du 8 Mai", "city": "Essômes-sur-Marne", "region": "Picardie", "country": "France", "lat": 49.029142, "lon": 3.37383},
              {"name": "Place du 11 Nov 1918 et 8 Mai 45", "city": "Autricourt", "region": "Bourgogne", "country": "France", "lat": 47.997219, "lon": 4.61962},
              {"name": "Place du 11 Novembre et du 8 Mai", "city": "Herbault", "region": "Centre", "country": "France", "lat": 47.6056, "lon": 1.142072},
              {"name": "Place des 8 et 11 Mai 1945", "city": "Saint-Nazaire", "region": "Pays de la Loire", "country": "France", "lat": 47.278412, "lon": -2.216284},
              {"name": "Rue du Souvenir : 11 Novembre - 8 Mai - 19 Mars", "city": "Germagny", "region": "Bourgogne", "country": "France", "lat": 46.672714, "lon": 4.604167}]},
    "05_11": {'done': False, 'streets' : [{"name": "Place des 8 et 11 Mai 1945", "city": "Saint-Nazaire", "region": "Pays de la Loire", "country": "France", "lat": 47.278412, "lon": -2.216284}]},
    "06_09": {'done': False, 'streets' : [{"name": "Rue des 9 et 10 Juin 1940", "city": "Venables", "region": "Haute-Normandie", "country": "France", "lat": 49.200421, "lon": 1.297545},
              {"name": "Rue d\'9 10 Juin 1940", "city": "Dreux", "region": "Centre", "country": "France", "lat": 48.734489, "lon": 1.368024}]},
    "06_10": {'done': False, 'streets' : [{"name": "Rue des 9 et 10 Juin 1940", "city": "Venables", "region": "Haute-Normandie", "country": "France", "lat": 49.200421, "lon": 1.297545},
              {"name": "Rue d\'9 10 Juin 1940", "city": "Dreux", "region": "Centre", "country": "France", "lat": 48.734489, "lon": 1.368024}]},
    "06_19": {'done': False, 'streets' : [{"name": "Rue des 19 et 20 Juin 1907", "city": "Cuxac-d'Aude", "region": "Languedoc-Roussillon", "country": "France", "lat": 43.24415, "lon": 2.998209}]},
    "06_20": {'done': False, 'streets' : [{"name": "Rue des 19 et 20 Juin 1907", "city": "Cuxac-d'Aude", "region": "Languedoc-Roussillon", "country": "France", "lat": 43.24415, "lon": 2.998209}]},
    "07_24": {'done': False, 'streets' : [{"name": "Place du 24-25 Juillet 1944", "city": "Donges", "region": "Pays de la Loire", "country": "France", "lat": 47.330319, "lon": -2.077903}]},
    "07_25": {'done': False, 'streets' : [{"name": "Place du 24-25 Juillet 1944", "city": "Donges", "region": "Pays de la Loire", "country": "France", "lat": 47.330319, "lon": -2.077903}]},
    "09_04": {'done': False, 'streets' : [{"name": "Place du 4 et 5 Septembre", "city": "Hargnies", "region": "Champagne-Ardenne", "country": "France", "lat": 50.019477, "lon": 4.790652}, 
              {"name": "Avenue des 4, 8 et 9 Septembre", "city": "Le Portel", "region": "Nord-Pas-de-Calais", "country": "France", "lat": 50.70666, "lon": 1.57299}]},
    "09_05": {'done': False, 'streets' : [{"name": "Place du 4 et 5 Septembre", "city": "Hargnies", "region": "Champagne-Ardenne", "country": "France", "lat": 50.019477, "lon": 4.790652}]},
    "09_08": {'done': False, 'streets' : [{"name": "Avenue des 4, 8 et 9 Septembre", "city": "Le Portel", "region": "Nord-Pas-de-Calais", "country": "France", "lat": 50.70666, "lon": 1.57299}]},
    "09_09": {'done': False, 'streets' : [{"name": "Avenue des 4, 8 et 9 Septembre", "city": "Le Portel", "region": "Nord-Pas-de-Calais", "country": "France", "lat": 50.70666, "lon": 1.57299}]},
    "11_11": {'done': False, 'streets' : [{"name": "Place du 11 Novembre et du 8 Mai", "city": "Essômes-sur-Marne", "region": "Picardie", "country": "France", "lat": 49.029142, "lon": 3.37383},
              {"name": "Place du 11 Nov 1918 et 8 Mai 45", "city": "Autricourt", "region": "Bourgogne", "country": "France", "lat": 47.997219, "lon": 4.61962},
              {"name": "Place du 11 Novembre et du 8 Mai", "city": "Herbault", "region": "Centre", "country": "France", "lat": 47.6056, "lon": 1.142072},
              {"name": "Rue du Souvenir : 11 Novembre - 8 Mai - 19 Mars", "city": "Germagny", "region": "Bourgogne", "country": "France", "lat": 46.672714, "lon": 4.604167}]}
}


def getdate(line):
    """ get a clean string and try to return a date """
    #s = "2016-03-26T09:25:55.000Z"
    #f = "%Y-%m-%dT%H:%M:%S.%fZ"
    dateformat1 = "%d %m %Y" # 31 01 1981
    #dateformat2 = "%d %m"
    dateformat3 = "%d %m %y" # 31 01 81
    ddmmyyyy = "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([1-9]|0[1-9]|1[0-2])(.|-|)[0-9][0-9][0-9][0-9]"
    ddmmyy = "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([1-9]|0[1-9]|1[0-2])(.|-|)[0-9][0-9]"
    ddmm = "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(.|-)([1-9]|0[1-9]|1[0-2])"
    yyyy = "(.|-|)[0-9][0-9][0-9][0-9]"
    patternddmmyyyy = re.compile("^"+ddmmyyyy+"$")
    patternddmm = re.compile("^"+ddmm+"$")
    patternddmmyy   = re.compile("^"+ddmmyy+"$")
    patternddmmyyyy_yyyy   = re.compile("^"+ddmmyyyy+yyyy+"$")
    patternddmmyyyyddmmyyyy   = re.compile("^"+ddmmyyyy+ddmmyyyy+"$")
    patternddmmyyyyddmmyy   = re.compile("^"+ddmmyyyy+ddmmyy+"$")
    
    match = re.search(patternddmm, line)
    if match != None:
#        logger.debug("matching ddmm$")
        res = datetime.strptime("{} {} 2004".format(match.group(1), match.group(3)), dateformat1)
        return [res]
    else:
        match = re.search(patternddmmyyyy, line)
        if match != None:
            # logger.debug("matching ddmmyyyy$")
            res = datetime.strptime("{} {} 2004".format(match.group(1), match.group(3)), dateformat1)
            return [res]
        else:
            match = re.search(patternddmmyy, line)
            if match != None:
#                logger.debug("matching ddmmyy$")
                res = datetime.strptime("{} {} 2004".format(match.group(1), match.group(3)), dateformat1)
                return [res]
            else:
                match = re.search(patternddmmyyyy_yyyy, line)
                if match != None:
                    # logger.debug("matching patternddmmyyyy_yyyy$")
                    res = datetime.strptime("{} {} 2004".format(match.group(1), match.group(3)), dateformat1)
                    return [res]
                else:
                    match = re.search(patternddmmyyyyddmmyyyy, line)
                    if match != None:
                        # logger.debug("matching patternddmmyyyyddmmyyyy$")
                        res1 = datetime.strptime("{} {} 2004".format(match.group(1), match.group(3)), dateformat1)
                        res2 = datetime.strptime("{} {} 2004".format(match.group(5), match.group(7)), dateformat1)
                        return [res1, res2]
            
    # logger.debug("line: %s doesn't match!" % line)
    return None

REP1 = ["cour 6", "cour 7", "cour 8", "cour 9", "cour 10", "(", ")", "ruelle", "placette",
        "cité", "armistice", "grande", "placa", "venelle", "fbg",
        "place", "avenue", "rue", "boulevard", "impasse", "square", "rond-point", "quai", "plaça",
        "carrefour", "allées", "allée", "promenade", "trocadéro", "lotissement", "chemin",
        "passage",
        "esplanade", "parc", "pont", "voie", "pce", "passerelle", "passe", "rond point",
        "rampe", "faubourg", "traverse", "résidence", "général", "prolongée", "communale",
        "communal", "espace", "erables", "cite", "-la-",
        "du ", " et ", "des", "de ", "la ", "le ", "a ", "l'", "d'", "ou ", "an ", "les ",
        "aux ", "en ", "1285", " er ", 
        "libération", "alias", "route", "ex  roderneweg", "reignat", "boisséjour", "tilleuls",
        "residence", "résistance", "rose",
        "dom sncf", "cours", "bis", "souvenir", "franc", "privée", "anciens", "combattants", "afn",
        "victimes", "légion", "honneur", "25 fusillés", "déportés", "fusillés", "plaine",
        "grand", "petite", "petit", "nuit", "martyrs", "combats", "bombardement", "crech", "paix",
        "dulcie", "victoire", "plan", "rassemblement", "indulto", "dunlop",
        "mas", "thibert", "rd", "débarquement", "559", "traversière", "montée", "les quatre v",
        "gal", "gaulle", "pere", "maitre", "cd28", "mail", "appel", "communes", "maison", "ge",
        "cessez-le-feu", "cessez", "feu", "guerre", "algérie", "pile", "fin", "rippe", "rué",
        "raphèle", "bourg", "thizy", "naufragés",
        ",", ":", "d'"]
REP2 = {"-": " "}
REPDAY1 = {"1Er": "01", "1er": "01", "premier": "01", "dix-":"1",
           "onze":"11", "douze": "12", "treize":"13", "quatorze": "14", "quinze":"15",
           "seize":"16", "dix sept": "17", "dix huit": "18", "dix neuf": "19",
           "vingt-":"2", "vingtun": "21",
           "vingt deux": "22", "vingt trois": "23", "vingt quatre": "24", "vingt cinq": "25",
           "vingt six": "26", "ving sept": "27", "vingt huit": "28", "vingt neuf": "29",
           "trente-":"3", "trenteun": "31"}
REPDAY2 = {"un": "1", "deux":"2", "trois": "3", "quatre":"4", "cinq":"5", "six":"6", "sept":"7",
           "huit":"8", "neuf":"9", "dix":"10", "vingt":"20", "trente":"30"}
REPMONTH = {"janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05",
            "juin": "06", "juillet": "07", "août": "08", "septembre": "09",
            "octobre": "10", "novembre": "11", "nov ": "11", "décembre": "12"}

def cleanstr(line):
    res = line.lower()
    # logger.debug(res)
    for reps in REP1:
        res = res.replace(reps, "")
    # logger.debug(res)
    """ remove multiple white space """
    res = re.sub(' +',' ', res)
    # logger.debug(res)
    for torep, rep in REPMONTH.items():
        res = res.replace(torep, rep)
    # logger.debug(res)
    for torep, rep in REPDAY1.items():
        res = res.replace(torep, rep)
    # logger.debug(res)
    for torep, rep in REPDAY2.items():
        res = res.replace(torep, rep)
    # logger.debug(res)
    for torep, rep in REP2.items():
        res = res.replace(torep, rep)
    # logger.debug(res)
    res = res.strip()
    return res


def readfile2(infilename, outfilename):
    nberrors = 0
    nblines = 0
    nbappend = 0
    """ clean all character which are not part of a date """
    jsonlines = json.load(codecs.open(infilename, 'r', encoding='utf-8'))
    towrite = {}
    for line in jsonlines:
        nblines += 1
        cleanedstr = cleanstr(line[u'name'])
        #print("{} --> |{}|".format(line['name'], cleanedstr))
        try:
            datearr = getdate(cleanedstr)
            #line[u'dates'] = []
            for dateu in datearr:
                datestr = '{:02d}_{:02d}'.format(dateu.month, dateu.day)
                if datestr not in towrite:
                    towrite[datestr] = {'done': False, 'streets' : []}
                towrite[datestr]['streets'].append(line)
                nbappend += 1
            if datestr in impossibleparsingdict:
                towrite[datestr]['streets'].extend(impossibleparsingdict[datestr]['streets'])
                impossibleparsingdict.pop(datestr)
                # logger.info("{} appending impossible parsing dict to towrite dict".format(datestr))
            #file.write((json.dumps(line) + ",\n").encode('utf-8').decode('unicode_escape'))
        except AttributeError:
            print("Error on |{}| from {} --- {}".format(cleanedstr, line[u'name'], line))
            nberrors += 1
        except TypeError:
            nberrors += 1
            print("Error on |{}| from {} --- {}".format(cleanedstr, line[u'name'], line))
    if len(impossibleparsingdict) > 0:
        # logger.info("elements remaining in impossible parsing dict :{}".format(impossibleparsingdict))
        for key, value in impossibleparsingdict.items():
            # logger.info("adding element :{} - {}".format(key, value))
            towrite[key] = value
#    towrite = merge_two_dicts(towrite, impossibleparsingdict)
    with open(outfilename, "w", encoding='utf-8') as file:
        file.write((json.dumps(towrite)).encode('utf-8').decode('unicode_escape'))
    report(nblines, nberrors, towrite)

def report(nblines, nberrors, towrite):
    print("#dates: {}".format(len(towrite)))
    nbaddresses = 0
    for key, value in towrite.items():
        nbaddresses += len(value)
    print("#address: {}".format(nbaddresses))
    print("#errors: {} - #lines: {}".format(nberrors, nblines))
    print("      errors rate: {0:.0f}%".format(nberrors / nblines * 100))

def datetestcase():
    cases = ["19 03 1952 1962", "11 118 05", "45 09", "1920 06 1907", 
            "8 05 19448 05 1945", "1415 04 1945", "11 1119188 05 45", 
            "910 06 1940", "9 10 06 1940", "11 11", "1 11", "01 11", 
            "11 11 18", "1 11 18", "01 11 18", "11 11 1918", "1 11 1918", "01 11 1918"]
    print(getdate("07 02 44"))
    print(getdate("29 02 44"))
    print(getdate("29 02 1944"))
    print(getdate("29 02 2044"))

    for case in cases:
        print("{} ==> {}".format(case, getdate(case)))
    
# usage: python quality_enhance.py france.json france_final.json
if __name__ == "__main__":
    #datetestcase()
    #print(cleanstr("Rue du Dix-Neuf Mars 1962"))
    readfile2(sys.argv[1], sys.argv[2])


