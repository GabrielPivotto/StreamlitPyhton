#importa as bib
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.title("Gráficos em Mapa")

@st.cache_data #essa funcao fica no cache sempre que possivel
def load_data():
    pd.set_option('display.max_columns', None) #fala pra mostrar todas as colunas
    tabela = pd.read_csv('dados_RS.csv') #retorna a tabela lida a partir de pandas
    return tabela

#geracao de graficos dentro dos containers (regioes que agrupam o conteudo em um "objeto")
with st.container():
    st.write("---")

    df = load_data()

    result = df.groupby(['SP_CIDADE_H', 'latitude_h', 'longitude_h'])['SP_QT_PROC'].sum().reset_index()

    result.head(10)

    fig = px.scatter_mapbox(result, lat="latitude_h", lon="longitude_h", color="SP_QT_PROC", size="SP_QT_PROC", title="Quantidade Total de Procedimentos por Região",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=50,  zoom=5.7).update_layout(height=1000)

    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig)
    

with st.container():
    df = load_data()

    idx_max = df.groupby(['SP_CIDADE_H'])['SP_QT_PROC'].idxmax()

    result = df.loc[idx_max]

    result.head()

    fig = px.scatter_mapbox(result, lat="latitude_h", lon="longitude_h", color="SP_QT_PROC", size="SP_QT_PROC", title="Procedimento Mais Comum em Cada Municipio",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=50,  zoom=5.7, hover_data={'SP_N_PROC': True}).update_layout(height=1000)

    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig)