"""
This script scrapes news articles from the SER Ronda website and saves the data in a MongoDB database.
"""

import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo.server_api import ServerApi

from datetime import datetime

import json

def get_headlines():
    """
    Get the headlines from the SER Ronda website.
    """
    # Get the web page
    url = "https://cadenaser.com/radio-coca-ser-ronda/"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the news
    news = soup.find_all("article")

    # list of links to the news
    noticias = []
    
    # Get the information of the 3 firsts elements
    for new in news[:2]:
        title = new.contents[1].find("a").get("title")
        url = 'https://cadenaser.com' + new.contents[1].find("a").get("href")
        description = new.contents[1].find("p").text
        pre_date_parse = url.split('/')
        date = f'{pre_date_parse[4]}-{pre_date_parse[5]}-{pre_date_parse[6]}'        
        body = get_detail(url)
        # noticias.append(url)            
        # print(f'  ( {date} ) /// {titulo} /// {description} - {body}' )
        elemento = {"titulo": title, "subtitulo": '', "descripcion": description, "fecha": date, "url": url, "cuerpo": body}
        noticias.append(elemento)

    return noticias



def get_detail(url):
    """
    Get the details of a news article from the SER Ronda website.
    """
    # Get the web page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    new = soup.find("div", class_="cnt-txt")
    paragraphs = new.find_all("p")
    body = ''
    for para in paragraphs:
        paragraph = para.text
        body += paragraph + '\n'
    return body

def compose_json(data):
    """
    Compose the JSON object to be saved in the MongoDB database.
    """
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    final_json = {
        "fuente": "SER Ronda",
        "categoria": "local",
        "posicionamiento" : "4",
        "fecha_escaneo": date_time,
        "noticias": data
    }

    return final_json

# main entry point
if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb+srv://juanjo:seamosserios@cluster0.sv73ccp.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    noticias = get_headlines()
    noticias_json = compose_json(noticias)
    print (json.dumps(noticias_json, indent=4))
    db = myclient["tobedefined"]
    recuperaciones = db["recuperaciones"]
    recuperaciones.insert_one(noticias_json)
    print ("--- it is done  ---")
