#!/usr/bin/env python
# coding: utf-8

# In[172]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time


# In[173]:


# The main website, a listing a real estate properties in Toronto

website = "https://www.royallepage.ca/en/on/toronto/properties/"


# In[174]:


# This header will emulate a browser request somewhat, making it less likely to be blocked by the site

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})


# In[175]:


#Iterate through the website pages
for page_number in range(1, 20):
    url = f"{website}{page_number}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('li', {'class': 'card-group__item'})
    # Iterate through the individual real estate properties
    for listing in listings:
        price = listing.find('span', {'class': 'currency'}).text[1:] + listing.find('span', {'class': 'price'}).text
        address = listing.find('address', {'class': 'address-1'}).text.strip()
        bedrooms_span = listing.find('span', {'class': 'beds'})
        # Check if bedrooms are listed
        if bedrooms_span:
            bedrooms = int(bedrooms_span.text.strip())
        else:
            bedrooms = 'Not listed'
        bathrooms_span = listing.find('span', {'class': 'baths'})
        # Check if bathrooms are listed
        if bathrooms_span:
            bathrooms = float(bathrooms_span.text.strip())
        else:
            bathrooms = 'Not listed'
        postal_code_span = listing.find('img', alt=re.compile(r'Toronto, ON [A-Z]\d[A-Z] \d[A-Z]\d'))
        # Check if postal codes are listed
        if postal_code_span:
            postal_code_pattern = r'Toronto, ON ([A-Z]\d[A-Z] \d[A-Z]\d)'
            postal_code = re.search(postal_code_pattern, postal_code_span['alt']).group(1)
        else:
            postal_code = 'Not listed'
        row = {'price': price, 'address': address, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'postal_code': postal_code}
        rows.append(row)
    # Add a delay between requests so as to not overwhelm the website
    time.sleep(1)


# In[183]:


# Create the dataframe

df = pd.DataFrame(rows)


# In[182]:


print(df)


# In[184]:


# Export the dataframe to a CSV file

df.to_csv('toronto_real_estate.csv', index=False)


# In[ ]:




