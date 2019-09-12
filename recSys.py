#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Part III. The recommender system"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
import random
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def opciones_usuario():
    print('*********Bienvenido al primer recomendador de rutas de montaña en México!*********\n')
    print("Para definir tu próxima ruta de montaña, responde a las siguientes preguntas \n\n\t\t\t\t1 en caso afirmativo \n\t\t\t\t0 en caso negativo\n")

    while True:
        try:
            opcion_1 = int(input("Vas con niños? \n"))
            if opcion_1 == 0:
                break
            elif opcion_1 == 1:
                break
        except ValueError:
            pass
        continue

    while True:
        try:
            opcion_2 = int(input("Llevas perros? \n"))
            if opcion_2 == 0:
                break
            elif opcion_2 == 1:
                break
        except ValueError:
            pass
        continue
    while True:
        try:
            opcion_3 = int(input("Quieres hacer la ruta en bici? \n"))
            if opcion_3 == 0:
                break
            elif opcion_3 == 1:
                break
        except ValueError:
            pass
    while True:
        try:
            opcion_4 = int(input("Y por último, qué nivel de dificultad buscas?\n\t\t\t\t 1 para escoger ruta fácil\n\t\t\t\t 2 para escoger ruta moderada\n\t\t\t\t 3 para escoger ruta difícil\n"))
            if opcion_4 == 1:
                break
            elif opcion_4 == 2:
                break
            elif opcion_4 == 3:
                break
        except ValueError:
            pass
    return opcion_1,opcion_2,opcion_3,opcion_4

# Do: 0,1,1,2


# In[3]:


def data_for_user_input(opcion_1,opcion_2,opcion_3,opcion_4):
    """Fuction to prepare data for the second part of user input"""
    
    #Using user's first input
    data_modified = data.loc[(data.kid_friendly==opcion_1)&(data.dog_friendly==opcion_2)&(data.mountain_biking==opcion_3)&(data.difficulty_level==opcion_4)].reset_index(drop = True)
    
    # Generating the names and region of the routes
    lista_hike_names = [l for l in data_modified['hike_name']]
    lista_hike_regions = [l for l in data_modified['region']]
    set(lista_hike_names)
    tuplas = list(set(zip(lista_hike_names, lista_hike_regions)))
    
    return tuplas


# In[5]:


def new_user_rating(tuplas):
    """Function to generate new user's dictionary, containing ratings"""
    new_user_dict = {} 
    contador = 0

    for i in tuplas:
        intro = int(input(f"Has visitado la ruta {i[0]}, ubicada en {i[1]}? \n 1 para sí, \n 0 para no\n"))
        if intro !=0:
            new_user_dict.update({i[0]:int(input(f"\t\tCalifíca la ruta {i[0]}: \n"))})
    
    return new_user_dict


# In[8]:


if __name__ == '__main__':
    
    data = pd.read_csv('data_ready.csv')                                   # This matrix contains 252 hike routes and 660 users
    
    opcion_1,opcion_2,opcion_3,opcion_4 = opciones_usuario()               # Calling first input # Do: 0,1,1,2
    
    data_modified = data.loc[(data.kid_friendly==opcion_1)&(data.dog_friendly==opcion_2)
            &(data.mountain_biking==opcion_3)&(data.difficulty_level==opcion_4)].reset_index(drop = True)    # First filter from first input

    tuplas = data_for_user_input(opcion_1,opcion_2,opcion_3,opcion_4)      # Preparing data for the next user input 
    
    new_user_dict = new_user_rating(tuplas)                                # 2nd user input, retorning the new user dictionary

    ####
    data_hike = data_modified.groupby(['userID','hike_name']).agg({'rating':"mean"}).reset_index()         

    data_hike_pivot = data_hike.pivot_table(index=['hike_name'],columns='userID',values='rating',aggfunc='mean').fillna(0)

    dist = squareform(pdist(data_hike_pivot.T,'euclidean'))               # User similarity using the 'euclidean' metric
    afinidad = 1/(1+dist)                                                 # Higher score describes users that are more similar. 
    afinidad = pd.DataFrame(afinidad, index=data_hike_pivot.columns, columns=data_hike_pivot.columns) # To dataframe
    
    # Generating Recommendations for a new User

    data_hike_pivot['new_user_dict']=pd.Series(new_user_dict)

    data_hike_pivot.fillna(0,inplace=True)

    afinidad = pd.DataFrame(1/(1+squareform(pdist(data_hike_pivot.T,'euclidean'))), 
                            index=data_hike_pivot.columns, columns=data_hike_pivot.columns)

    similarities = afinidad['new_user_dict'].sort_values(ascending=False)[1:]
    
    no_hechas_new_user = data_hike_pivot[data_hike_pivot['new_user_dict']==0]
    
    afinidad['new_user_dict'].sort_values(ascending=False)[1:]
    
    recommendations = no_hechas_new_user.copy()
    
    for name,score in dict(similarities).items():
        recommendations[name]=recommendations[name]*score
    
    recommendations['Total'] = recommendations.sum(axis=1)
    recommendations.sort_values('Total', ascending=False) #here
    
    #using cosine metric

    afinidad = pd.DataFrame(1/(1 + squareform(pdist(data_hike_pivot.T, 'cosine'))),  #distancia del coseno, según ángulos
                             index=data_hike_pivot.columns, columns=data_hike_pivot.columns)

    similarities = afinidad['new_user_dict'].sort_values(ascending=False)[1:]

    recommendations = no_hechas_new_user.copy()

    for name, score in dict(similarities).items():
        recommendations[name] = recommendations[name] * score

    recommendations['Total'] = recommendations.sum(axis=1)
    print(recommendations.sort_values('Total', ascending=False))


# In[ ]:




