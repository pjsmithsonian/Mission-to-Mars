# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find('div', class_= 'content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_= 'content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
news_p


# ### 10.3.4 - Scrape Mars Data: Featured Image

# ### Featured Images
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html,'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### 10.3.5 - Scrape Mars Data: Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description','value']
df.set_index('description', inplace = True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
html = browser.html
mars_soup = soup(html, 'html.parser')
images = mars_soup.find_all('div', class_='item')

for image in images:
    hemispheres = {}
    
    # Iterate over hemispheres for image and title link
    link = image.a['href']
    full_link = base_url + link
        
    # navigate to link
    browser.visit(full_link)
    html2 = browser.html
    page_soup = soup(html2, 'html.parser')
        
    # Image
    pic_div = page_soup.find_all('li')[0]
    img_url = pic_div.a['href']
    full_img_url = base_url + img_url
        
    # Title
    title = page_soup.h2.text
    
    # add to dictionary
    hemispheres['img_url'] = full_img_url
    hemispheres['title'] = title
    
    # add dictionary to list
    hemisphere_image_urls.append(hemispheres)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()