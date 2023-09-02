import streamlit as st
import pandas as pd
import numpy as np



import time

st.title("LQAS")
st.write("Dashboard do LQAS:")

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

DATE_COLUMN = 'Date_of_LQAS'

@st.cache_data
def load_data():
    #data = pd.read_csv(DATA_URL, nrows=nrows)
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    #return data

    ######33
    lqas_url = "MOZ_SIA_LQAS_Assessment.xlsx"
    data = pd.read_excel(lqas_url, sheet_name="data")
    hh = pd.read_excel(lqas_url, sheet_name="Count_HH")
    dfg = pd.merge(data, hh, left_on='_index', right_on='_parent_index', how='left')
    
    #return dfg
    # Carregue seus dados em DataFrames


    # Filtros de colunas e linhas


    columns = ['Region', 'District', 'facility',
              '_GPS_hh_latitude', '_GPS_hh_longitude','roundNumber', 'Date_of_LQAS','Count_HH/Children_seen',
               'Count_HH/Age_Child', 'Count_HH/Sex_Child', 'Count_HH/FM_Child', 'Count_HH/withCard',
               'Count_HH/Care_Giver_Informed_SIA','Count_HH/Reason_Not_FM','Count_HH/Caregiver_Source_Info']#'Date_of_LQAS','Region', 'District', 'facility',
    df = dfg[columns]
    df = df[(df['Date_of_LQAS'] >= '2023-06-15') & (df['Date_of_LQAS'] >= '2023-06-18')]

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

    df = df.dropna(subset=['_GPS_hh_latitude', '_GPS_hh_longitude'])
    df["latitude"]=df['_GPS_hh_latitude']
    df["longitude"]=df['_GPS_hh_longitude']
    #df['_GPS_hh_latitude'].fillna(mean_latitude, inplace=True)
    #df['_GPS_hh_longitude'].fillna(mean_longitude, inplace=True)
    ######################################## Criar vacinados com cartao ou dedo
    df["Vacinado"] = np.where((df["Count_HH/FM_Child"] == "Yes") | (df["Count_HH/FM_Child"] == 1) | 
                              (df["Count_HH/withCard"] == "Yes"), "Yes", "No")
    #df["Vacinado"] = ["Yes" if (x == "Yes" or y == "Yes") else "No" for x, y in zip(df["Count_HH/FM_Child"], df["Count_HH/withCard"])]

    df["Count_HH/Care_Giver_Informed_SIA"] = np.where((df["Count_HH/Care_Giver_Informed_SIA"] == "Yes") | 
                                                      (df["Count_HH/Care_Giver_Informed_SIA"] == 1) , "Yes", "No")
    return df

    #print (df)
df=load_data()
option = st.selectbox(
    'Selecione a Ronda',
     df['Rnd'].unique())

'You selected: ', option

chart_data = df["Region"].value_counts()

st.line_chart(chart_data)



#map_data = df[['latitude','longitude']]

#st.map(map_data)
st.map(df,
    latitude='latitude',
    longitude='longitude',use_container_width=True
    )#size='col3',color='Vacinado'

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
# Cria um DataFrame com a contagem de valores únicos na coluna "Vacinado"
resumo = pd.DataFrame(df["Vacinado"].value_counts())

# Renomeia a coluna para "Total"
resumo.columns = ["Total"]

# Escreve o DataFrame na tela
st.write(resumo)


