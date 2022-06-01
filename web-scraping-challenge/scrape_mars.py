#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=5)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, "html.parser")
    #from soup find id which is = news
    news_title = soup.find(id = 'news')
    #select the first title
    news_one = news_title.select('#news .content_title')[0].text
    #select the first paragraph
    para_text = news_title.select('#news .article_teaser_body')[0].text


#JPL Mars Space Images—Featured Image

    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    #Visit the URL for the Featured Space Image site(https://spaceimages-mars.com).
    url_image = 'https://spaceimages-mars.com'
    browser.visit(url_image)

    #Use Splinter to navigate the site and find the image URL for the current Featured Mars Image

    #Iterate through all pages
    for x in range(50):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soupA = bs(html, 'html.parser')
        # Retrieve all elements that contain book information
        images = soupA.find('img', class_='headerimage fade-in')['src']
        first_part = 'https://spaceimages-mars.com/'
        #then assign the URL string to a variable called `featured_image_url`.
        featured_image_url = first_part + images

 #mars facts

    #import dependencies
    import pandas as pd
    #Visit (https://galaxyfacts-mars.com)
    m_url = 'https://galaxyfacts-mars.com'
    #use Pandas to scrape the table containing facts about the planet including diameter, mass, etc.
    mars_tables = pd.read_html(m_url)
    #Use Pandas to convert the data into a dataframe
    mars_df = mars_tables[0]
    mars_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    #Use Pandas to convert the dataframe to a HTML table string.
    mars_html = mars_df.to_html()
    #save to HTML file
    #mars_df.to_html('mars_table.html')
    #browser.quit()

# # Mars Hemispheres
    #add url link
    mars_url = 'https://marshemispheres.com/'
    #requests.get(mars_url, timeout=3)
    #opening the browser
    browser.visit(mars_url)
    time.sleep(5)
    hemisphere_image_urls = []
    for i in range(4):
        mars_hem = {}
        browser.find_by_css('a.product-item h3')[i].click()
        #create a starting element
        element = browser.find_by_text('Sample').first
        url_img = element['href']
        h2_title = browser.find_by_css('h2.title').text
        #create lists for img_url link and for the title
        mars_hem["Image URL"] = url_img
        mars_hem["Title"] = h2_title
        #add to the list
        hemisphere_image_urls.append(mars_hem)
        browser.back()

#place into dic

    data = {
        'first_paragraph': para_text,
        'first_article': news_one,
        'feature_image_url': featured_image_url,
        'mars_html': mars_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return data
