# This script scraps the weather forecast at https://www.meteoblue.com/en/weather/forecast/multimodel/luxembourg-findel-airport_luxembourg_6296718
# and saves the image locally

from http.client import REQUEST_URI_TOO_LONG
import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo.server_api import ServerApi

from datetime import datetime

import json


def get_multimode_luxembourg():
    # Get the web page
    url = "https://www.meteoblue.com/en/weather/forecast/multimodel/luxembourg-findel-airport_luxembourg_6296718"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the Analysis chart
    chart = soup.find("div", class_="blooimage")

    img_element = chart.find("img")

    # Get the src elemento
    url = 'https:' + img_element.attrs['data-original']
    
    return url


def get_multimode_Ronda():
    # Get the web page
    url = "https://www.meteoblue.com/en/weather/forecast/multimodel/ronda_spain_2511730"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the Analysis chart
    chart = soup.find("div", class_="blooimage")

    img_element = chart.find("img")

    # Get the src elemento
    url = 'https:' + img_element.attrs['data-original']
    
    return url


def get_image_from_url(url, filename):
    # Get the image
    img = requests.get(url)

    # Save the image
    with open("src/publishing/content/weather/" + filename, "wb") as f:
        f.write(img.content)
        
    return img


if __name__ == "__main__":
    # Multimodel para Luxemburgo
    lux_multimodel = get_multimode_luxembourg()
    get_image_from_url(lux_multimodel, "luxembourg_multimodel.png")

    #Multimodel para ronda
    ronda_multimodel = get_multimode_Ronda()
    get_image_from_url(ronda_multimodel, "ronda_multimodel.png")

    
    print("Done")