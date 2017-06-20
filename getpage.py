# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, urldefrag
from pprint import pprint
import re
from re import sub
from werkzeug.contrib.cache import SimpleCache


# Si vous écrivez des fonctions en plus, faites-le ici

cache = SimpleCache()

def getJSON(page):
    params = urlencode({
      'format' : 'json',
      'action' : 'parse',
      'prop' : 'text',
      'redirects' : 'true',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    
    return response.read().decode('utf-8')


def getRawPage(page):

    parsed = cache.get(page)
    if parsed is None:
        parsed = loads(getJSON(page))
        cache.set(page, parsed, timeout=180)


    
    try:
        title = unquote(parsed["parse"]["title"])
        content = unquote(parsed["parse"]["text"]["*"])
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result


def getPage(page):
    title, content = getRawPage(page)
    l = []
    try :
        soup = BeautifulSoup(content, "html.parser")
        attr = soup.select("p a[href]")
        for el in attr[:10] :
            if (re.match(r"(/wiki)", el['href']) != None):
                l.append(el['href'][6:].replace('_',' '))
                l = getUniqueItems(l)

        l = [item for item in l if not (re.match(r"Projet:", item) or re.match(r"Discussion:", item) or re.match(r"Aide:", item) or re.match(r"Modèle:", item) 
            or re.match(r"Wikipédia:", item) or re.match(r"API", item))]
        l = [urldefrag(item)[0] for item in l]

        return title, l
        
    except KeyError:
        return None, []



#if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    # print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # pprint(getJSON("Utilisateur:A3nm/INF344"))
    #pprint(getRawPage("Utilisateur:A3nm/INF344"))
    #pprint(getPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))

