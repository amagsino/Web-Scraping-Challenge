# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Browser set up
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
mars_info = {}

# NASA Mars News
def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    
    #slide_element.find("div", class_="content_title")

    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()
    mars_info["news_title"] = news_title
    mars_info["news_paragraph"] = news_p

    # JPL Space Images - Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    #expand = browser.find_by_css("a.fancybox-expand")
    

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")

    img_relative = jpl_soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = f"https://www.jpl.nasa.gov{img_relative}"
    mars_info["featured_image_url"] = featured_image_url

    # Mars Weather
    mars_weather_url = ('https://twitter.com/marswxreport?lang=en')

    response = requests.get(mars_weather_url)
    weather_soup = BeautifulSoup(response.text, 'html.parser')

    contents = weather_soup.find_all("div",class_="content")

    weather_mars = []
    for content in contents:
        tweet = content.find("div", class_="js-tweet-text-container").text
        weather_mars.append(tweet)

    mars_weather = weather_mars[0]
    mars_info["mars_weather"] = mars_weather

    # Mars Facts
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    table[0]

    df = table[0]
    df.columns = ["Facts", "Value"]
    df.set_index(["Facts"])
    df

    facts_html = df.to_html()
    facts_html = facts_html.replace("\n","")
    mars_info["mars_facts"] = facts_html

    # Mars Hemisphere
    hemisphere_image_urls = []

    # Valles Marineris Hemisphere
    valles_url = ("https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced")

    response = requests.get(valles_url)
    valles_soup = BeautifulSoup(response.text, "html.parser")

    valles_marineris_img = valles_soup.find_all("div", class_="wide-image-wrapper")
    print(valles_marineris_img)

    for img in valles_marineris_img:
        pic = img.find("li")
        full_img = pic.find("a")["href"]
        print(full_img)
    valles_marineris_title = valles_soup.find("h2", class_="title").text
    print(valles_marineris_title)
    valles_marineris_hem = {"Title": valles_marineris_title, "url": full_img}
    print(valles_marineris_hem)

    # Cerberus Hemispheres
    cerberus_url = ("https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced")

    response = requests.get(cerberus_url)
    cerberus_soup = BeautifulSoup(response.text, "html.parser")

    cerberus_img = cerberus_soup.find_all("div", class_="wide-image-wrapper")
    print(cerberus_img)

    for img in cerberus_img:
        pic = img.find("li")
        full_img = pic.find("a")["href"]
        print(full_img)
    cerberus_title = cerberus_soup.find("h2", class_="title").text
    print(cerberus_title)
    cerberus_hem = {"Title": cerberus_title, "url": full_img}
    print(cerberus_hem)

    # Schiaparelli Hemisphere
    schiaparelli_url = ("https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced")

    response = requests.get(schiaparelli_url)
    schiaparelli_soup = BeautifulSoup(response.text, "html.parser")

    shiaparelli_img = schiaparelli_soup.find_all("div", class_="wide-image-wrapper")
    print(shiaparelli_img)

    for img in shiaparelli_img:
        pic = img.find("li")
        full_img = pic.find("a")["href"]
        print(full_img)
    shiaparelli_title = schiaparelli_soup.find("h2", class_="title").text
    print(shiaparelli_title)
    shiaparelli_hem = {"Title": shiaparelli_title, "url": full_img}
    print(shiaparelli_hem)

    # Syrtis Hemisphere
    syrtis_url = ("https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced")

    response = requests.get(syrtis_url)
    syrtis_soup = BeautifulSoup(response.text, "html.parser")

    syrtris_img = syrtis_soup.find_all("div", class_="wide-image-wrapper")
    print(syrtris_img)

    for img in syrtris_img:
        pic = img.find("li")
        full_img = pic.find("a")["href"]
        print(full_img)
    syrtris_title = syrtis_soup.find("h2", class_="title").text
    print(syrtris_title)
    syrtris_hem = {"Title": syrtris_title, "url": full_img}
    print(syrtris_hem)

    hemisphere_image_urls.append(cerberus_hem)
    hemisphere_image_urls.append(shiaparelli_hem)
    hemisphere_image_urls.append(syrtris_hem)
    hemisphere_image_urls.append(valles_marineris_hem)
    hemisphere_image_urls

    mars_info["hemispheres_info"] = hemisphere_image_urls

    browser.quit()

    return mars_info