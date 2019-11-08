from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

# FOR WINDOWS USERS
# importing google chrome driver putting into function
def initiateBrowser():
    executablePath = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executablePath, headless=False)

# Create emtpy dictionary that can be imported to Mongo
marsInfo = {}

def marsNews():
    # URL of Nasa News
    try: 
        browser = initiateBrowser()
        url = "https://mars.nasa.gov/news/"
        # Retrieve page with requests
        browser.visit(url)
        # Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve elements for title and paragraph to store in mongo        
        title = soup.find('div', class_ = 'content_title').text
        paragraph = soup.find('div', class_ = 'article_teaser_body').text

        # Store variables above as dictionary entry
        marsInfo['newsTitle'] = title
        marsInfo['newsParagraph'] = paragraph

        return marsInfo

    finally:
        browser.quit()

def marsFeaturedImage():
    try:
        browser = initiateBrowser()
        # Visit Mars Space Images through splinter module
        imageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(imageURL)
        
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

        # dictionary entry for the features image
        marsInfo['featuredImgURL'] = featuredImageLink

        return marsInfo
    
    finally:
        browser.quit()

def marsWeather():
    try:
        browser = initiateBrowser()
        # Visit the URL for Mars weather Twitter using Splinter
        weatherURL = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weatherURL)
        
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
        
        # Dictionary entry for the weather tweet
        marsInfo['marsWeather'] = weatherTweet

        return marsInfo
    finally:
        browser.quit()
            
def marsFacts():
    # Visit Mars fact page
    factsURL = 'https://space-facts.com/mars/'
    
    # Use read_html function in Pandas to parse 
    marsFacts = pd.read_html(factsURL)

    # Find the table with Mars facts (only table on the page)
    marsFactsDF = marsFacts[0]

    # Set the column headers for table on website
    marsFactsDF.columns = ['Category' , 'Facts']

    # Set index to Category of fact to drop the 0,1,2,3,4... index
    marsFactsDF.set_index('Category', inplace=True)
    
    factData = marsFactsDF.to_html()

    marsInfo['marsFacts'] = factData

    return marsInfo

def marsHemis():
    try:
        # Initiate browser
        browser = initiateBrowser()

        # Visit URL with Mars Hemisphere images
        hemisURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisURL)
        
        # Store HTML OBJECT in a variable & then PARSE this page and store in a Soup variable
        htmlHemis = browser.html
        soup = BeautifulSoup(htmlHemis, 'html.parser')
        
        # Retreive all of the <div class='item'> that contain Mars hemispheres information
        hemisItems = soup.find_all('div', class_='item')
        
        # Create empty list for hemisphere urls 
        hemisImageURL = []
        
        # Store the mainURL of the page with all 4 of the relevant links we want to gather
        # # The 'a' tag in the div class=item is only the tail of each individual page
        hemisMainURL = 'https://astrogeology.usgs.gov'
        
        # Loop through the items previously stored
        for hemi in hemisItems: 
            # Store name of Hemisphere
            name = hemi.find('h3').text
            
            # Store partial link that leads to full image website (again only a partial link provided)
            partialImgURL = hemi.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that combines partial link the full image website 
            browser.visit(hemisMainURL + partialImgURL)
            
            # HTML Object of individual hemisphere information website 
            partialImgHTML = browser.html
            
            # Parse HTML with BeautifulSoup for every individual hemisphere information website as we loop through
            soup = BeautifulSoup(partialImgHTML, 'html.parser')
            
            # Retrieve full image direct links
            imgURL = hemisMainURL + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries defined above as hemisImageURLs
            hemisImageURL.append({"name" : name, "imgURL" : imgURL})
            
            time.sleep(5)
        # Display hemisImageURL list of dictionaries
        marsInfo['hemisImageURL'] = hemisImageURL

        return marsInfo

    finally:
        browser.quit()