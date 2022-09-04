# This script scraps the web page https://cadenaser.com/radio-coca-ser-ronda/


import requests
from bs4 import BeautifulSoup

def get_headlines():
    # Get the web page
    url = "https://cadenaser.com/radio-coca-ser-ronda/"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the news
    news = soup.find_all("article")

    # list of links to the news
    links = []
    
    # Get the information of the 3 firsts elements
    for new in news[:2]:
        
        titulo = new.contents[1].find("a").get("title")
        url = 'https://cadenaser.com' + new.contents[1].find("a").get("href")
        description = new.contents[1].find("p").text
        pre_date_parse = url.split('/')
        date = f'{pre_date_parse[4]}-{pre_date_parse[5]}-{pre_date_parse[6]}'        
        body = get_detail(url)
        links.append(url)            
        print(f'  ( {date} ) /// {titulo} /// {description} - {body}' )

    return links



def get_detail(url):

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


# main entry point
if __name__ == "__main__":
    get_headlines()
    print ("--- it is done  ---")