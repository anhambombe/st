#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import accuracy_score

# Carregue seus dados em DataFrames
lqas_url = "C:\\Users\\LENOVO\\Documents\\Eu\\WHO_2022\\DADOS\\PBI\\MOZ_SIA_LQAS_Assessment.xlsx"
data = pd.read_excel(lqas_url, sheet_name="data")
hh = pd.read_excel(lqas_url, sheet_name="Count_HH")
dfg = pd.merge(data, hh, left_on='_index', right_on='_parent_index', how='left')

# Filtros de colunas e linhas

#df = df[(df['Date_of_LQAS'] >= '2023-06-15') & (df['Date_of_LQAS'] >= '2023-06-18')]
columns = ['Region', 'District', 'facility',
          '_GPS_hh_latitude', '_GPS_hh_longitude','roundNumber', 'Date_of_LQAS','Count_HH/Children_seen',
           'Count_HH/Age_Child', 'Count_HH/Sex_Child', 'Count_HH/FM_Child', 'Count_HH/withCard',
           'Count_HH/Care_Giver_Informed_SIA','Count_HH/Reason_Not_FM','Count_HH/Caregiver_Source_Info']#'Date_of_LQAS','Region', 'District', 'facility',
df = dfg[columns]


########################################## Criação da Coluna ronda

# E as datas estejam no formato 'YYYY-MM-DD'

df["Rnd"] = np.select([
    (df["Date_of_LQAS"] >= "2022-03-30") & (df["Date_of_LQAS"] <= "2022-04-01"),
    (df["Date_of_LQAS"] >= "2022-05-04") & (df["Date_of_LQAS"] <= "2022-05-07"),
    (df["Date_of_LQAS"] >= "2022-07-13") & (df["Date_of_LQAS"] <= "2022-07-18"),
    (df["Date_of_LQAS"] >= "2022-08-25") & (df["Date_of_LQAS"] <= "2022-08-27"),
    (df["Date_of_LQAS"] >= "2022-10-17") & (df["Date_of_LQAS"] <= "2022-10-22"),
    (df["Date_of_LQAS"] >= "2022-12-17") & (df["Date_of_LQAS"] <= "2022-12-21"),
    (df["Date_of_LQAS"] >= "2023-04-19") & (df["Date_of_LQAS"] <= "2023-04-20"),
    (df["Date_of_LQAS"] >= "2023-06-22") & (df["Date_of_LQAS"] <= "2023-06-26"),
    (df["Date_of_LQAS"] >= "2023-08-25") & (df["Date_of_LQAS"] <= "2023-08-29")
], [
    "1ª Rnd", "2ª Rnd", "3ª Rnd", "4ª Rnd", "5ª Rnd", "6ª Rnd", "7ª Rnd", "8ª Rnd", "9ª Rnd"
], default="Sarampo")



######################################## Criar vacinados com cartao ou dedo
df["Vacinado"] = np.where((df["Count_HH/FM_Child"] == "Yes") | (df["Count_HH/FM_Child"] == 1) | 
                          (df["Count_HH/withCard"] == "Yes"), "Yes", "No")
#df["Vacinado"] = ["Yes" if (x == "Yes" or y == "Yes") else "No" for x, y in zip(df["Count_HH/FM_Child"], df["Count_HH/withCard"])]

df["Count_HH/Care_Giver_Informed_SIA"] = np.where((df["Count_HH/Care_Giver_Informed_SIA"] == "Yes") | 
                                                  (df["Count_HH/Care_Giver_Informed_SIA"] == 1) , "Yes", "No")





# In[ ]:





# In[ ]:




