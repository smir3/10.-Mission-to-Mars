# Import Splinter, BeautifulSoup, and Pandas
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#initialize the browser, create a data dictionary, end the webdriver and return the scraped data. when headless=True is declared as we initiate the browser, we are telling it to run in headless mode
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary, CREATE A NEW DICTIONARY IN THE DATA DICTIONRARY TO HOLD A LIST WITH URL STRING AND TITLE
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_data(browser)
    }
    
    

    # Stop webdriver and return data
    browser.quit()
    return data

# Set up Splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    #Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Search for elements with a specific combination of tag div and attribute - Optional delay of waiting 1 minutes for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set-up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of 
    #list_text
    #slide_elem = news_soup.select_one('div.list_text')


    # CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using 
    #select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.

    # The specific data is in a <div /> with a class of 'content_title'
    #slide_elem.find('div', class_='content_title')

    # Most recent title published on the website - Use the parent element to find the first `a` tag and save it as `news_title`.    
    #.get_text() returns only the title of the news article and not any of the HTML tags or elements
    #news_title = slide_elem.find('div', class_='content_title').get_text()

    # to get the most recent article title, use find instead of find.all. find.all will give all titles, find will give most recent
    # Use the parent element to find the paragraph text
    #news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

    # ### Features Images

def hemisphere_data(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemisphere_image_title = []
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere. browser.find_by_css gets all 
    #hemispheres
    # First, get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item h3')
    
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)): 
        try:

            links = browser.find_by_css('a.product-item h3')

            # We have to find the elements on each loop to avoid a stale element exception
            links[i].click()

            # Next, we find the Sample image anchor tag and extract the href
            imgs_href = browser.find_link_by_partial_text('Sample').first['href']

            # Get Hemisphere title
            title = browser.find_by_css('h2.title').text

            # Append hemisphere object to list
            hemisphere_image_urls.append(imgs_href)
            hemisphere_image_title.append(title)

            # Finally, we navigate backwards
            browser.back()

        except:
            break

    zip_iterator = zip(hemisphere_image_title, hemisphere_image_urls)
    
    hemisphere_data_result = []

    for title, url in zip_iterator:
        hemisphere_data_result.append({
                'title' : title,
                'url' : url
    })    
    
    return hemisphere_data_result
    
    
    #return as a list of dictionaries with the URL string and title of each hemisphere image
    
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup to scrape the full-size image URL
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url
    
    # Find the relative image url for the most recent image by specifying the location
    #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    #img_url_rel

    # above code is only the second half of the code, need the first part of the url
    # Use the base URL to create an absolute URL
    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    # create a new datafram from the html table, read html searched and return a list of table found in html, index of 0 means pull only       #the first table
    #df = pd.read_html('https://galaxyfacts-mars.com')[0]
    # assign columns to the new dataframe
    #df.columns=['description', 'Mars', 'Earth']
    # turn description solumn into dataframe index
    #df.set_index('description', inplace=True)
    #df

    # easily convert the dataframe back into html-ready code
    #df.to_html()

    #browser.quit()

def mars_facts():
    # Add try/except for error handling
    try:

        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")
    
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


