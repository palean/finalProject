#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Part II. Code to clean the 'data_raw.csv' and get it ready for the recommender system"""

import pandas as pd
import numpy as np
#from pandas.io.json import json_normalize
from operator import itemgetter
import re


# In[10]:


# TESTING  (dentro de la función 'parsing_data')
#header = soup_test.find('div', id='title-and-menu-box')


# In[2]:


# to see what's going on
#df = pd.read_csv('data_raw.csv')
#df.reset_index(drop=True)


# In[3]:


def add_features(hike_df):
    """Function that classifies 12 characteristics into each route """
    
    hike_df['dog_friendly'] = 0
    hike_df['kid_friendly'] = 0
    hike_df['camping'] = 0
    hike_df['trekking'] = 0
    hike_df['near_water'] = 0
    hike_df['mountain_biking'] = 0
    hike_df['great_views'] = 0
    hike_df['bird_watching'] = 0
    hike_df['climbing'] = 0
    hike_df['forests'] = 0
    hike_df['trail_running'] = 0
    hike_df['historic_place'] = 0
    
    for idx, attribute in enumerate(hike_df['hike_attributes']):
        for feature in [el[1:-1] for el in attribute[1:-1].split(', ')]:
            
            if feature == 'apto para perros' or feature == 'perros con correa':
                hike_df['dog_friendly'].iloc[idx] = 1 

            if feature == 'apto para niños':
                hike_df['kid_friendly'].iloc[idx] = 1

            if feature == 'acampada':
                hike_df['camping'].iloc[idx] = 1

            if feature == 'senderismo' or feature == 'excursiones por la naturaleza':
                hike_df['trekking'].iloc[idx] = 1

            if feature == 'río' or feature == 'cascada' or feature =='lago':
                hike_df['near_water'].iloc[idx] = 1

            if feature == 'ciclismo de montaña':
                hike_df['mountain_biking'].iloc[idx] = 1

            if feature == 'vistas' or feature == 'conducción panorámica':
                hike_df['great_views'].iloc[idx] = 1

            if feature == 'observación de aves' or feature == 'fauna':
                hike_df['bird_watching'].iloc[idx] = 1

            if feature == 'escalada' or feature == 'rocoso' or feature =='trepar':
                hike_df['climbing'].iloc[idx] = 1

            if feature == 'bosque' or feature == 'flores silvestres':
                hike_df['forests'].iloc[idx] = 1

            if feature == 'trail running':
                hike_df['trail_running'].iloc[idx] = 1

            if feature == 'lugar histórico':
                hike_df['historic_place'].iloc[idx] = 1

    hike_df.drop('hike_attributes', axis=1, inplace=True)
    return hike_df


# In[4]:


def data_cleaning(df):
    """Function to clean data"""
    
    df = df.drop(columns=['Unnamed: 0'])                                                            # Dropping first column (from last index)
    df['distance'] =  df['distance'].apply(lambda x: re.sub(r'[^0-9.]','', str(x))).astype(float)   # Taking out non-numeric characters
    df['elevation'] =  df['elevation'].apply(lambda x: re.sub(r'[^0-9.]','', str(x))).astype(float) # Taking out non-numeric characters and converting to float
    df['route_type'] =  df['route_type'].apply(lambda x: re.sub(r'\n','',re.sub(r'Tipo de ruta:','',str(x)))) # Keeping the characteristics of the route
    df['difficulty_level'] = df['difficulty_level'].map({'fácil':1,'moderada':2,'difícil':3})       # Converting categoric variable into number level
    df.rename(columns={'distance': 'distance_kms', 'elevation': 'elevation_mts'}, inplace=True)     # Renaming distance and elevation columns just to be aware of its units

    df = df.assign(hikeID=(df.hike_name).astype('category').cat.codes)                              #Assigning hike codes from 0 to 251
    df = df [['hikeID','hike_name','region','distance_kms','elevation_mts','difficulty_level','stars','num_reviews','user_ratings','route_type','hike_attributes']] # Settle order
    df = pd.get_dummies(df, columns=['route_type'],drop_first=True)                                 # There are 3 types: 'Circular', 'De punto a punto' & 'Ida y vuelta'.
    df = add_features(df)                                                                           # Selecting 12 characteristics

    df['user_ratings'] = df['user_ratings'].apply(eval)                                             # Converting the string 'user_ratings' to a list of dictionaries.
    
    return df


# In[5]:


# To see df
#df = data_cleaning(df)
#df


# In[6]:


# Para tener en cuenta
#df[df['num_reviews']>29]


# In[7]:


#type(df['user_ratings'][0][0]) #now, its a list of dicts


# In[8]:


# To see df
#hike_user_rating_df


# In[9]:


def create_rating_df(df):
    """Function to put in separate columns the user and ratings"""
    
    lista_dicts = [l for l in hike_user_rating_df['user_ratings']]      # List of lists where each element contains the dictionary
    rating_df = pd.DataFrame(columns=['hike_name', 'user', 'rating'])   # Empty df
    
    tmp_hikeID = []
    tmp_hike = []
    tmp_user = []
    tmp_rating = []
    
    for i in range(len(df)):                                            # By each element of the df    
        for el in lista_dicts[i]:
            tmp_hikeID.append(df['hikeID'][i])                          # Adding 'hikeID'
            tmp_hike.append(df['hike_name'][i])                         # Adding 'hike_name'
            tmp_user.append(*el)                                        # Adding user name
            tmp_rating.append(list(map(itemgetter(0), el.values()))[0]) # Adding the rating given by the user

    rating_df['hikeID'] = tmp_hikeID
    rating_df['hike_name'] = tmp_hike
    rating_df['user'] = tmp_user
    rating_df['rating'] = tmp_rating

    return rating_df


# In[10]:


def rating_df_cleanup(rating_df):
    
    rating_df['rating'] = rating_df.rating.astype(float)                                  # Turning rating to a float type
    rating_df = rating_df.assign(userID=(rating_df['user']).astype('category').cat.codes) # Assigning user codes from 0 to 659
    rating_df["userID"] = "user_" + (rating_df["userID"]).astype(str)                     # and adding 'user' to characterize userID
    rating_df = rating_df [['hikeID','hike_name','userID','user','rating']]               # Order settling
    
    return(rating_df)


# In[12]:


if __name__ == '__main__':
    
    df = pd.read_csv('data_raw.csv')                                                             # importing data
    df.reset_index(drop=True)
    
    df = data_cleaning(df)                                                                       # Cleaning data. This is the first df

    hike_user_rating_df = df[['hikeID','hike_name','user_ratings']].copy()                       # Creating a new df
    rating_df = create_rating_df(hike_user_rating_df)                                            # Taking user and rating into different columns
    rating_df = rating_df_cleanup(rating_df)                                                     # Cleaning rating_df. This is the second df.
    
    data_ready = pd.merge(df, rating_df, on='hikeID')                                            # Merging 'df' and 'rating_df' by common column 'hikeID'
    
    data_ready = data_ready.drop(columns=['user_ratings','hike_name_y'])                         # Doing some cleanning to 'data_ready'
    data_ready.rename(columns={'hike_name_x': 'hike_name'}, inplace=True)                        
    data_ready = data_ready[['hikeID', 'hike_name', 'region', 'distance_kms', 'elevation_mts',
       'difficulty_level', 'stars', 'num_reviews', 'userID',
       'user', 'rating','route_type_De punto a punto', 'route_type_Ida y vuelta',
       'dog_friendly', 'kid_friendly', 'camping', 'trekking', 'near_water',
       'mountain_biking', 'great_views', 'bird_watching', 'climbing',
       'forests', 'trail_running', 'historic_place']]
    
    data_ready.to_csv('data_ready.csv',index=False)                                              # Creating an unique csv cleaned file


# In[13]:


#data_ready

