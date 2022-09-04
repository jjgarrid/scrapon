# This script scraps the web page https://www.charrytv.com/noticias
# and saves the data in a file called "noticias.txt"

import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo.server_api import ServerApi

from datetime import datetime

import json

def get_headlines():
    # Get the web page
    url = "https://www.charrytv.com/noticias"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the news
    news = soup.find_all("div", class_="noticia section")

    # list of links to the news
    noticias = []

    
    # Get the information of each news
    for new in news:
        title = new.find_all("a")[1].text
        description = new.find_all("a")[2].text
        date = new.find("p", class_="date").text
        url = new.find_all("a")[1].get("href")
        title1, subtitle, body = get_detail(url)
        # To Python object
        elemento = {"titulo": title, "subtitulo": subtitle, "descripcion": description, "fecha": date, "url": url, "cuerpo": body}
        noticias.append(elemento)
        #print(f'  ( {date} ) /// {title1} /// {subtitle} - {body}' )

    return noticias


def get_detail(url):

    # Get the web page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    new = soup.find("div", class_="col1 content")
    
    title1 = new.find("h1").text
    title2 = new.find("h2").text
    body = ''
    body_paras = new.find_all("p")
    body_paras = body_paras[3:]
    for para in body_paras:
        paragraph = para.text
        body += paragraph + '\n'

    return title1, title2, body

def compose_json(data):

    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    final_json = {
        "fuente": "CharryTV",
        "categoria": "local",
        "posicionamiento" : "4",
        "fecha_escaneo": date_time,
        "noticias": data
    }

    return final_json

if __name__ == "__main__":

    myclient = pymongo.MongoClient("mongodb+srv://juanjo:seamosserios@cluster0.sv73ccp.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    noticias = get_headlines()
    noticias_json = compose_json(noticias)
    print (json.dumps(noticias_json, indent=4))
    db = myclient["tobedefined"]
    recuperaciones = db["recuperaciones"]
    recuperaciones.insert_one(noticias_json)
