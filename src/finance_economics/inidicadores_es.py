"""
This script scrapes data from the INE website and saves screenshots of various economic indicators.
"""

# This script gets data from www.ine.es
# And saves the data in a mongodb database

# import webdriver
import time
from webbrowser import get
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def initialization():
    """
    Initialize the web scraping process by getting the web page and creating a webdriver object.
    """
    # Get the web page
    url = "https://www.charrytv.com/noticias"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    service = ChromeService(executable_path=ChromeDriverManager().install())

    # Screenshot machine
    ob = Screenshot.Screenshot()  

    # create webdriver object
    driver = webdriver.Chrome(service=service)

    # return soup
    return soup, driver


def destroy(driver):
    """
    Close and quit the webdriver.
    """
    driver.close()
    driver.quit()


def get_pib_chart(driver):
    """
    Scrape the PIB chart from the INE website and save the screenshot.
    """
    # get
    driver.get("https://ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736164439&menu=ultiDatos&idp=1254735576581")
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, "aceptarCookie")))
    driver.maximize_window()
    bt = driver.find_element(By.ID, "aceptarCookie")
    time.sleep(2)
    bt.click()

    # get element 
    element = driver.find_element(By.ID, 'grafTab')
    
    # Scroll into view
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)

    total_height = element.size['height'] + 1000
    driver.set_window_size(1920, total_height)  # the trick
    time.sleep(2)

    # click screenshot 
    element.screenshot('src/publishing/content/ecofin/pibGraph.png')

    element = driver.find_element(By.CLASS_NAME, 'tablaCat')
    element.screenshot('src/publishing/content/ecofin/pibTabla.png')


def get_sociedades_mercantiles(driver):
    """
    Scrape the Sociedades Mercantiles chart from the INE website and save the screenshot.
    """
    driver.get('https://ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177026&menu=ultiDatos&idp=1254735576550')
    wait = WebDriverWait(driver, 30)

    # get element 
    element = driver.find_element(By.ID, 'grafTab')
    
    total_height = element.size['height'] + 1250
    driver.set_window_size(1920, total_height)  # the trick
    time.sleep(2)

    # click screenshot 
    element.screenshot('src/publishing/content/ecofin/socMercGraph.png')

    element = driver.find_element(By.CLASS_NAME, 'tablaCat')
    element.screenshot('src/publishing/content/ecofin/socMercTabla.png')

def get_sociedades_negocio(driver):
    """
    Scrape the Sociedades de Negocio chart from the INE website and save the screenshot.
    """
    driver.get('https://ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176958&menu=ultiDatos&idp=1254735576550')
    wait = WebDriverWait(driver, 30)

    # get element 
    element = driver.find_element(By.ID, 'grafTab')
    
    total_height = element.size['height'] + 1250
    driver.set_window_size(1920, total_height)  # the trick
    time.sleep(2)

    # click screenshot 
    element.screenshot('src/publishing/content/ecofin/socNegoGraph.png')

    element = driver.find_element(By.CLASS_NAME, 'tablaCat')
    element.screenshot('src/publishing/content/ecofin/socNegoTabla.png')

def get_hipotecas(driver):
    """
    Scrape the Hipotecas chart from the INE website and save the screenshot.
    """
    driver.get('https://ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736170236&menu=ultiDatos&idp=1254735576606')
    wait = WebDriverWait(driver, 30)

    # get element 
    element = driver.find_element(By.ID, 'grafTab')
    
    total_height = element.size['height'] + 1250
    driver.set_window_size(1920, total_height)  # the trick
    time.sleep(2)

    # click screenshot 
    element.screenshot('src/publishing/content/ecofin/hipotecaGraph.png')

    element = driver.find_element(By.CLASS_NAME, 'tablaCat')
    element.screenshot('src/publishing/content/ecofin/hipotecaTabla.png')

if __name__ == "__main__":
    soup, driver = initialization()
    get_pib_chart(driver)
    get_sociedades_mercantiles(driver)
    get_sociedades_negocio(driver)
    get_hipotecas(driver)

    # limpieza y final
    destroy(driver)
