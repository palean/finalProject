#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Part I. Code to pull key information from alltrails.com and create a 'data_raw.csv' to work with"""

import selenium                                                  #for web scrapping
from selenium import webdriver                               
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait          # for the elements to be visible
from selenium.webdriver.common.by import By                      #Explicit Waits
from selenium.webdriver.support import expected_conditions as EC #Explicit Waits

from bs4 import BeautifulSoup
import requests
import pandas as pd
#from pymongo import MongoClient
import time


# In[2]:


# Función para hacer login: debo estar logueada para poder navegar varias páginas

def login_and_get_soup(navegador):
    navegador.get('http://www.alltrails.com')
    go_login = navegador.find_element_by_xpath('//li[@id="login"]')  
    go_login.click()
    time.sleep(9)
    username = navegador.find_element_by_id("user_email")
    password = navegador.find_element_by_id("user_password")
    username.send_keys("paola.aleanflorez15@bathspa.ac.uk")
    password.send_keys("paopao")
    navegador.find_element_by_name("commit").click()
    navegador.get('https://www.alltrails.com/es/mexico')
    soup = get_hike_routes(navegador)
    return soup, navegador


# In[3]:


# Función que carga todas las reseñas de la página:

def get_hike_routes(navegador):
    navegador.get('https://www.alltrails.com/es/mexico')
    while True:
        try:
            load_more_hikes = WebDriverWait(navegador, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@id="load_more"]')))
            load_more_hikes.click()
            time.sleep(5)
        except:
            break
    soup = BeautifulSoup(navegador.page_source) #getting all the HTML soup
    return soup


# In[12]:


# Función que 'scrapea' cada link (252) con el raw data para el db

def parsing_data(html_soup):
    header = html_soup.find('div', id='title-and-menu-box')        # Header where it can be found: hike_name, difficulty_level, stars and num_reviews
    
    region = html_soup.find_all('span',{'class':'xlate-none'})[3].text.lower()  #zone name
    
    try:
        hike_name = header.findChild('h1').text                        
    except:
        hike_name = None
    difficulty_level = header.findChild('span').text.lower()        
    stars = header.findChild('meta')['content']                    
    num_reviews = header.find('span', itemprop="reviewCount").text 
    
    try:                                                           # Distance of the route
        distance = html_soup.select('span.distance-icon')[0].text
    except:
        distance = None

    try:                                                           # Elevation gain of the route
        elevation = html_soup.select('span.elevation-icon')[0].text
    except:
        elevation = None

    try:                                                           # Route type, if it is circular or not
        route_type = html_soup.select('span.route-icon')[0].text
    except:
        route_type = None

    tags = html_soup.select('section.tag-cloud')[0].findChildren('h3') # Tags with route characteristics
    hike_attributes = [tag.text for tag in tags]
    
    users = html_soup.select('div.feed-user-content.rounded')         # List of dictionaries with the user name and rating number
    user_ratings = []
    for user in users:
        if user.find('span', itemprop='author') != None:
                user_name = user.find('span', itemprop='author').text
                #user_name = user_name.replace('.', '')
                try:
                    rating = user.find('span', itemprop="reviewRating").findChildren('meta')[0]['content']
                    user_ratings.append({user_name: rating})
                except:
                    pass
        
    row_data = {}
    row_data['hike_name'] = hike_name
    row_data['region'] = region
    row_data['difficulty_level'] = difficulty_level
    row_data['stars'] = stars
    row_data['num_reviews'] = num_reviews
    row_data['distance'] = distance
    row_data['elevation'] = elevation
    row_data['route_type'] = route_type
    row_data['hike_attributes'] = hike_attributes
    row_data['user_ratings'] = user_ratings
    
    return row_data


# In[13]:


#Función que crea el database a partir de los vínculos, llama la función de 'parsing_data' y los convierte 252 html_soups en db
hike_list =[]

def create_db(soup, navegador):
    resenas = navegador.find_elements_by_class_name('mobile-block')       # Points to the titles of mountain routes
    vinculos = [el.get_attribute('href') for el in resenas]               # It goes through the ratings and get the routes link
    vinculos_unique = list(set(vinculos))                                 # Unique list of hike links, ready to scrap <<252 routes with given rating>>
    for el in vinculos_unique:
        html = requests.get(el).content
        html_soup = BeautifulSoup(html,'html')
        hike = parsing_data(html_soup)                                
        hike_list.append(hike)
        #table.insert_one(mongo_doc)
    return hike_list


# In[14]:


# PROBANDO - segunda parte: 
#hike = create_db(soup, navegador)


# In[15]:


#create_db(soup, navegador)


# In[16]:


#len(hike_list)


# In[17]:


def empty_df():
    # Creating empty df with column titles
    df = pd.DataFrame(columns=['hike_name',
                               'region',
                               'difficulty_level',                               
                               'stars',
                               'num_reviews',
                               'distance',
                               'elevation',
                               'route_type',
                               'hike_attributes',
                               'user_ratings'])
    return df

def parse_record(hike_list):
    # Getting each row
    row = pd.Series({'hike_name': hike_list.get('hike_name', None),
                     'region': hike_list.get('region', None),
                     'difficulty_level': hike_list.get('difficulty_level', None),
                     'stars': hike_list.get('stars', None),
                     'num_reviews': hike_list.get('num_reviews', None),
                     'distance': hike_list.get('distance', None),
                     'elevation': hike_list.get('elevation', None),
                     'route_type': hike_list.get('route_type', None),
                     'hike_attributes': hike_list.get('hike_attributes', None),
                     'user_ratings': hike_list.get('user_ratings', None)})
    return row


def turn_into_pandas(hike_list):
    '''
    Function to pull 'hike' from the raw_data into a pandas DataFrame
    INPUT: 'hike' from the raw_data
    OUTPUT: pandas DataFrame object
    '''
    df = empty_df()
    df_2 = empty_df()
    
    i = 0
    for h in hike_list:
        i += 1
        row = parse_record(h)
        df_2 = df_2.append(row, ignore_index=True)
    df = df.append(df_2)
    return df


# In[18]:


if __name__ == '__main__':
    
    navegador = webdriver.Chrome()        # Abre un nuevo navegador
    soup = login_and_get_soup(navegador)  # Hace login, y consigue los links de las rutas to scrap
    create_db(soup, navegador)            # Crea un db con row_data, retorna 'hike_list'
    hike_df = turn_into_pandas(hike_list)
    hike_df


# In[20]:


hike_df.to_csv('data_raw.csv',index=False)


# In[21]:


hike_df.head()


# In[ ]:




