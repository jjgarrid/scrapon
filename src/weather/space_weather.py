# import webdriver
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

service = ChromeService(executable_path=ChromeDriverManager().install())
  
# create webdriver object
driver = webdriver.Chrome(service=service)
  
# get geeksforgeeks.org
driver.get("https://www.swpc.noaa.gov/communities/radio-communications")
  
# get element 
element = driver.find_element(By.XPATH, '//*[@id="block-swx-noaa-scales-noaascales"]')
  
# click screenshot 
element.screenshot('src/publishing/content/weather/foo.png')
