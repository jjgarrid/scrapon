"""
This script scrapes weather charts from the Met Office website and saves images locally.
"""

# This script scraps the weather chart in https://www.weathercharts.org/
# and saves the image locally

from http.client import REQUEST_URI_TOO_LONG
import requests
from bs4 import BeautifulSoup

import pymongo
from pymongo.server_api import ServerApi

from datetime import datetime

import json

def get_the_page_source():
    """
    Get the web page source from the Met Office website.
    """
    # Get the web page
    url = "https://www.metoffice.gov.uk/weather/maps-and-charts/surface-pressure/"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_analysis_north_atlantic(soup):
    """
    Get the Analysis chart for the North Atlantic from the Met Office website.
    """
    # Get the Analysis chart
    chart = soup.find("div", class_="surface-pressure-chart")

    img_element = chart.find("li", id="chartColour0").find("img")

    # Get the src elemento
    url = img_element.get("src")
    
    return url

def get_forecast_12h(soup):
    """
    Get the 12-hour forecast chart for the North Atlantic from the Met Office website.
    """
    # Get the Analysis chart
    chart = soup.find("div", class_="surface-pressure-chart")

    img_element = chart.find("li", id="chartColour1").find("img")

    # Get the src elemento
    url = img_element.get("src")
    
    return url

def get_forecast_24h(soup):
    """
    Get the 24-hour forecast chart for the North Atlantic from the Met Office website.
    """
    # Get the Analysis chart
    chart = soup.find("div", class_="surface-pressure-chart")

    img_element = chart.find("li", id="chartColour2").find("img")

    # Get the src elemento
    url = img_element.get("src")
    
    return url


def get_image_from_url(url, filename):
    """
    Save the image from the given URL to the specified filename.
    """
    # Get the image
    img = requests.get(url)

    # Save the image
    with open("src/publishing/content/weather/" + filename, "wb") as f:
        f.write(img.content)
        
    return img


if __name__ == "__main__":
    # Inicializacion
    page_source = get_the_page_source()

    # Analisis NA EU hoy
    na_analysis = get_analysis_north_atlantic(page_source)
    get_image_from_url(na_analysis, "na_analysis.png")

    # Forecast 12h NA EU
    na_12h_forecast = get_forecast_12h(page_source)
    get_image_from_url(na_12h_forecast, "na_12h_forecast.png")

    # Forecast 24h NA EU
    na_24h_forecast = get_forecast_24h(page_source)
    get_image_from_url(na_24h_forecast, "na_24h_forecast.png")
    
    # Todo el atlantico norte
    get_image_from_url("https://ocean.weather.gov/A_sfc_full_ocean_color.png", "full_na_analysis.png")

    # European fronts
    get_image_from_url("https://page.met.fu-berlin.de/wetterpate/static/emtbkna.gif", "eu_fronts.png")

    # Jetstreams
    get_image_from_url("http://www.stormsurfing.com/stormuser2/images/dods/natla_250_00hr.png", "jetstreams.png")
    
    print("Done")
