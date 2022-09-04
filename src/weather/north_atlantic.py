# This script scraps the weather chart in https://www.weathercharts.org/
# and saves the image locally

from http.client import REQUEST_URI_TOO_LONG
import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo.server_api import ServerApi

from datetime import datetime

import json

def get_analysis_north_atlantic():
    # Get the web page
    url = "https://www.metoffice.gov.uk/weather/maps-and-charts/surface-pressure/"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the Analysis chart
    chart = soup.find("div", class_="surface-pressure-chart")

    img_element = chart.find("li", id="chartColour0").find("img")

    # Get the src elemento
    url = img_element.get("src")
    
    return url

def get_image_from_url(url):
    # Get the image
    img = requests.get(url)

    # Save the image
    with open("src/publishing/content/weather/north_atlantic.png", "wb") as f:
        f.write(img.content)
        
    return img


if __name__ == "__main__":
    na_analysis = get_analysis_north_atlantic()
    get_image_from_url(na_analysis)
    print("Done")