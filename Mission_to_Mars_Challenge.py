#!/usr/bin/env python
# coding: utf-8

# In[8]:


pip install webdriver_manager


# In[2]:


pip install splinter


# In[2]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[4]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[11]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[12]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[13]:


slide_elem.find('div', class_='content_title')


# In[14]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[15]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[16]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[17]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[18]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[19]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[20]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[ ]:


# create a new datafram from the html table, read html searched and return a list of table found in html, index of 0 means pull only the first table
#df = pd.read_html('https://galaxyfacts-mars.com')[0]
# assign columns to the new dataframe
#df.columns=['description', 'Mars', 'Earth']
# turn description solumn into dataframe index
#df.set_index('description', inplace=True)
#df


# In[ ]:


# easily convert the dataframe back into html-ready code
#df.to_html()


# In[ ]:


#browser.quit()


# ### Mars Facts

# In[21]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[22]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[23]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[103]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[104]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_image_title = []
 
# 3. Write code to retrieve the image urls and titles for each hemisphere. browser.find_by_css gets all hemispheres
# First, get a list of all of the hemispheres
links = browser.find_by_css('a.product-item h3')


# In[102]:


#links[0].click()
#browser.find_link_by_partial_text('Sample').first['href']


# In[105]:


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


# In[106]:


hemisphere_image_title


# In[107]:


zip_iterator = zip(hemisphere_image_title, hemisphere_image_urls,)


# In[108]:


hemisphere = dict(zip_iterator)


# In[109]:


print(hemisphere)


# In[110]:


# 5. Quit the browser
browser.quit()

