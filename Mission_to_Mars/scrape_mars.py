from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # NASA Mars News

    # Retrieve page with the requests module
    response = requests.get(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the first news title
    news_title = soup.find("div", class_="content_title").text

    # Find the paragraph associated with the first title
    news_p = soup.find("div", class_="article_teaser_body").text


    # JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Get URL from "Featured Image"
    featured_image_url = browser.links.find_by_partial_href("feature").first["href"]


    # Mars Facts

    #  URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Read Tables with pandas
    tables = pd.read_html(url)

    # Select Table and display results
    df = tables[0]

    html_table = df.to_html()
    html_table.replace('\n', '')
    html_table

    # Mars Hemispheres

    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Locate Divs with infos
    div_item = soup.find_all('div', class_='item')

    img_urls = []

    # Loop through div_item
    for x in div_item:
        
        # Find title
        div_description = x.find('div', class_="description")
        title = div_description.h3.text
        
        # Find links and browse into it
        div_link = div_description.a["href"]    
        browser.visit(url + div_link)
        
        # HTML object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find img url    
        img_url = soup.find('li').a['href']

        # Create dictionary to store title and url
        img_dict = {}
        img_dict['title'] = title
        img_dict['img_url'] = url + img_url
        
        img_urls.append(img_dict)
    img_urls


    # Store data into a dictionary
    data_dict = {
    "news_title": news_title,
    "news_p": news_p,
    "feature_image": featured_image_url,
    "images": img_urls,
    "table": html_table
    }

    browser.quit()

    # Return results
    return data_dict