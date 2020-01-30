#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser("chrome", **executable_path, headless = False)
def scrape():
    browser = init_browser()
    mars_facts_data = {}
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)
    soup=bs(browser.html,'html.parser')
    #scrapping latest news about mars from nasa
    News_title = soup.find_all('div', class_='content_title')[0].text
    News_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    mars_facts_data['news_title'] = News_title
    mars_facts_data['news_paragraph'] = News_paragraph
    #Mars Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(jpl_url))
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    images = browser.find_by_xpath(xpath)
    image = images[0]
    image.click()
    time.sleep(2)
    #get image url using BeautifulSoup
    soup = bs(browser.html, "html.parser")
    image_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = base_url + image_url
    mars_facts_data["featured_image"] = featured_image_url
    # #### Mars Weather
    #get mars weather's latest tweet from the website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    soup = bs(browser.html, "html.parser")
    #temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    #mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #mars_facts_data["mars_weather"] = mars_weather
    # #### Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(2)
    facts = pd.read_html(facts_url)
    mars_dataframe = facts[0]
    mars_dataframe.columns = ["Parameter", "Values"]
    mars_dataframe.set_index(["Parameter","Values"])
    #Converting the data to html table string
    mars_html= mars_dataframe.to_html()
    mars_html = mars_html.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html
    # #### Mars Hemisperes
    Hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Hemispheres_url)
    soup = bs( browser.html, "html.parser")
    mars_hemisphere = []
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        soup=bs(browser.html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
        mars_facts_data["hemisphere_img_url"] = mars_hemisphere 
    return mars_facts_data