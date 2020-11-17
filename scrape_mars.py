#################################################
# Mission to Mars: Web Scraping Challenge
#################################################

#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import time

#################################################
# Mars News
#################################################

#Scrape Title and Paragraphs
def mars_news():

    executable_path = {"executable_path": (r"C:\Users\Mickey\anaconda3\Scripts\chromedriver.exe")}
    browser = Browser("chrome", **executable_path, headless=False)

    #Browse URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    #Parse Results with BeautifulSoup (Allow for Try and Except)
    try:

        #Scrape the Latest Title and Paragraphs
        title = soup.find_all("div", class_="content_title")
        news_title = title[1].text.strip()
        news_paragraph = soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None

    #Close Broswer when done
    browser.quit()

    #Return Results
    return news_title, news_paragraph

#################################################
# Mars Images - Featured Image
#################################################

#Scrape Featured Image
def featured_img():

    executable_path = {"executable_path": (r"C:\Users\Mickey\anaconda3\Scripts\chromedriver.exe")}
    browser = Browser("chrome", **executable_path, headless=False)

    #Browse URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    #Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    #Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    #Parse Results with BeautifulSoup (Allow for Try and Except)
    html = browser.html
    image_soup = bs(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")

    try:
        img_url = img.get("src")
    except AttributeError:
        return None
    
    #Combine with Base URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"

    #Close Broswer when done
    browser.quit()
    
    #Return Results
    return img_url

#################################################
# Mars Facts
#################################################

#Scrape Mars Facts (Read using Pandas and allow for Try and Except)
def mars_facts():
    
    try:
        facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    facts_df.columns=["Description", "Value"]

    #Return Results
    return facts_df.to_html(index=False)

#################################################
# Mars Hemispheres
#################################################

#Scrape Hemispheres
def hemisphere():

    executable_path = {"executable_path": (r"C:\Users\Mickey\anaconda3\Scripts\chromedriver.exe")}
    browser = Browser("chrome", **executable_path, headless=False)

    #Browse URL
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #Create an Empty List to store Result
    hemi_img_urls = []

    #Get a List of Hemispheres
    products = browser.find_by_css("a.product-item h3")

    #Begin For Loop 
    for item in range(len(products)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[item].click()
        time.sleep(1)
        
        #Find Sample Image
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        #Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text

        #Add to List
        hemi_img_urls.append(hemisphere)

        #Navigate to Previous Page
        browser.back()

    #Close Broswer when done
    browser.quit()

    #Return Results
    return hemi_img_urls

#################################################
# Main Web Scraping 
#################################################

#Scrape Main Web Data
def scrape_data():

    #Call Latest Title and Paragraph
    news_title, news_paragraph = mars_news()

    #Call Featured Image
    img_url = featured_img()

    #Call Mars Facts
    facts = mars_facts()

    #Call Hemispheres
    hemisphere_image_urls = hemisphere()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }

    #Return Results
    return data