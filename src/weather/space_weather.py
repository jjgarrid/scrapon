"""
This script scrapes space weather data from the NOAA website and saves images locally.
"""

# import webdriver
from webbrowser import get
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager

from Screenshot import Screenshot

from http.client import REQUEST_URI_TOO_LONG
import requests
from bs4 import BeautifulSoup

def get_space_weather_banner():
    """
    Scrape the space weather banner from the NOAA website and save the screenshot.
    """
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # Screenshot machine
    ob = Screenshot.Screenshot()  

    # create webdriver object
    driver = webdriver.Chrome(service=service)
    
    # get NOAA space weather page
    driver.get("https://www.swpc.noaa.gov/communities/radio-communications")
    
    # get element 
    element = driver.find_element(By.XPATH, '//*[@id="block-swx-noaa-scales-noaascales"]')
    
    # click screenshot 
    element.screenshot('src/publishing/content/weather/space_weather_conditions.png')

    driver.close()
    driver.quit()

def get_radiocomms_map():
    """
    Scrape the radio communications map and chart from the NOAA website.
    """
    # Get the web page
    url = "https://www.swpc.noaa.gov/communities/radio-communications"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the map
    map = soup.find("div", class_="animation")

    img_element = map.find("img")

    # Get the src elemento
    url = img_element.get("src")

    chart = soup.find_all("td", class_="product-grid-cell")
    chart_img_eo = chart[1].find("img")
    url_chart = chart_img_eo.get("src")
    
    return url, url_chart

def get_electric_map():
    """
    Scrape the electric power community dashboard from the NOAA website.
    """
    # Get the web page
    url = "https://www.swpc.noaa.gov/communities/electric-power-community-dashboard"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the map
    chart = soup.find_all("td", class_="product-grid-cell")

    # First element
    chart_img_table = chart[0].find("img")
    url_table = chart_img_table.get("src")
    
    # Second elemento
    chart_img_eo = chart[1].find("img")
    url_chart = chart_img_eo.get("src")
    
    return url_table, url_chart

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
    get_space_weather_banner()
    url_map, url_chart = get_radiocomms_map()
    get_image_from_url(url_map, "radiocomms_map.png")
    get_image_from_url(url_chart, "radiocomms_chart.png") 

    url_electric1, url_electric2 = get_electric_map()
    get_image_from_url(url_electric1, "electric_map.png")
    get_image_from_url(url_electric2, "electric_chart.png")

    #Charging and satellites
    get_image_from_url('https://services.swpc.noaa.gov/images/seaesrt-charging-hazards.png','charging_hazard.png')
    get_image_from_url('https://services.swpc.noaa.gov/images/seaesrt-space-environment.png?time=1662474500000','space_environments.png')
    get_image_from_url('https://services.swpc.noaa.gov/images/seaesrt-time-series-270.png?time=1662474607000','time_series.png')
