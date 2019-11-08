#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time


# In[3]:


# FOR WINDOWS USERS
# importing google chrome driver
executablePath = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executablePath, headless=False)


# In[6]:


# URL of Nasa
url = "https://mars.nasa.gov/news/"

# Retrieve page with requests
browser.visit(url)

# Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[7]:


print('*****PARAGRAPH TITLE*****')
title = soup.find('div', class_ = 'content_title').text
print(title)
print()
print('*****PARAGRAPH TEASER*****')
paragraph = soup.find('div', class_ = 'article_teaser_body').text
print(paragraph)


# In[8]:


# Visit Mars Space Images through splinter module
imageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(imageURL)


# In[9]:


# Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
htmlImage = browser.html
soup = BeautifulSoup(htmlImage, 'html.parser')

# Retrieve background-image url from the style tag 
featuredImageLink  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Base website Url 
mainURL = 'https://www.jpl.nasa.gov'

# Join website url with scrapped route
featuredImageLink = mainURL + featuredImageLink

# Display full link to featured image
featuredImageLink


# In[10]:


# Visit the URL for Mars weather Twitter using Splinter
weatherURL = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weatherURL)


# In[11]:


# Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
htmlWeather = browser.html
soup = BeautifulSoup(htmlWeather, 'html.parser')

# Find all elements that contain tweets
tweets = soup.find_all('div', class_='js-tweet-text-container')

# Look for entries that display weather related words to treutn only weather tweet
for tweet in tweets: 
    weatherTweet = tweet.find('p').text
    if 'Sol' and 'pressure' in weatherTweet:
        print(weatherTweet)
        break
    else: 
        pass


# In[20]:


# Visit Mars fact page
factsURL = 'https://space-facts.com/mars/'

# Use read_html function in Pandas to parse 
marsFacts = pd.read_html(factsURL)

# check how many tables there are so you know what table index you need to pull
#len(marsFacts)

# Find the table with Mars facts (only table on the page)
marsFactsDF = marsFacts[0]

# Set the column headers for table on website
marsFactsDF.columns = ['Category' , 'Facts']

# Set index to Category of fact to drop the 0,1,2,3,4... index|
marsFactsDF.set_index('Category', inplace=True)

marsFactsDF


# In[13]:


# Visit URL with Mars Hemisphere images
hemisURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisURL)


# In[14]:


# Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
htmlHemis = browser.html
soup = BeautifulSoup(htmlHemis, 'html.parser')

# Retreive all of the <div class='item'> that contain Mars hemispheres information
hemisItems = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisImageURLs = []

# Store the mainURL of the page with all 4 of the relevant links we want to gather
# The 'a' tag in the div class=item is only the tail of each individual page
hemisMainURLs = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for hemi in hemisItems: 
    # Store name of Hemisphere
    name = hemi.find('h3').text
    
    # Store partial link that leads to full image website (again only a partial link provided)
    partialImgURL = hemi.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that combines partial link the full image website 
    browser.visit(hemisMainURLs + partialImgURL)
    
    # HTML Object of individual hemisphere information website 
    partialImgURL = browser.html
    
    # Parse HTML with BeautifulSoup for every individual hemisphere information website as we loop through
    soup = BeautifulSoup(partialImgURL, 'html.parser')
    
    # Retrieve full image direct links
    imgURL = hemisMainURLs + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries defined above as hemisImageURLs
    hemisImageURLs.append({"title" : name, "img_url" : imgURL})
    time.sleep(5)
    

# Display hemisImageURLs list of dictionaries
hemisImageURLs


# In[17]:


# Convert IPythonNoteBook into .py file
get_ipython().system('jupyter nbconvert --to script missionToMars.ipynb')


# In[ ]:




