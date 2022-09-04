# This script scraps the web page https://www.diarioronda.es/category/ronda/


import requests
from bs4 import BeautifulSoup

def get_headlines():
    # Get the web page
    url = "https://www.diarioronda.es/category/ronda/"
    page = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the news
    news = soup.find_all("article")

    # list of links to the news
    links = []
    
    # Get the information of each news
    for new in news:
        title_url = new.find("h2")
        titulo = title_url.text
        url = title_url.find("a").get("href")
        description = new.text.replace('\n\nFacebookTwitterComentarios\n\n\n','')
        date = new.find("time").text        
        body = get_detail(url)
        links.append(url)            
        print(f'  ( {date} ) /// {titulo} /// {description} - {body}' )

    return links



def get_detail(url):

    # Get the web page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    new = soup.find("div", class_="entry-content")
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