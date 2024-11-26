#importa as bib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.title("Gráficos Comuns")

@st.cache_data #essa funcao fica no cache sempre que possivel
def load_data():
    pd.set_option('display.max_columns', None) #fala pra mostrar todas as colunas
    tabela = pd.read_csv('dados_RS.csv') #retorna a tabela lida a partir de pandas
    return tabela

#geracao de graficos dentro dos containers (regioes que agrupam o conteudo em um "objeto")
with st.container():
    st.write("---")
    dados = load_data()

    dados['TEMPO_DT'] = dados['SP_DTSAIDA'] - dados['SP_DTINTER']

    agrupa = dados.groupby('SP_N_PROC').agg(
        QTD = ('SP_QT_PROC', 'sum'),
        MEDIA_DT = ('TEMPO_DT', 'mean')
    )

    maiores = agrupa.nlargest(20, 'QTD')

    ordenado = maiores.sort_values(by= 'QTD', ascending = False)

    fig = px.bar(maiores, y=maiores.index, x='MEDIA_DT', barmode = 'group', title="Tempo Médio de Internação dos 10 Procedimentos mais Comuns").update_layout(
        xaxis_title="Média de Tempo de Internação em Dias", 
        yaxis_title="Nome do Procedimento",
        yaxis={'categoryorder': 'total ascending'},
        height=650,
        width=1000
    )

    st.plotly_chart(fig)

with st.container():
    procedimentos = dados['SP_N_PROC'].value_counts().reset_index()
    procedimentos.columns = ['Procedimento', 'Frequência']


    fig = px.bar(procedimentos, x='Procedimento', y='Frequência',
        title='Frequência dos Procedimentos Realizados por Tipo',
        labels={'Procedimento': 'Tipo de Procedimento', 'Frequência': 'Quantidade'},
        color='Frequência').update_layout(height=1000)
    
    st.plotly_chart(fig)

with st.container():
    df = load_data()
    df['SP_DTINTER'] = pd.to_datetime(df['SP_DTINTER'], format='%Y%m%d', errors='coerce')
    df['SP_DTSAIDA'] = pd.to_datetime(df['SP_DTSAIDA'], format='%Y%m%d', errors='coerce')

    df['Duracao_Internacao'] = (df['SP_DTSAIDA'] - df['SP_DTINTER']).dt.days

    df = df[df['Duracao_Internacao'] >= 0]

    media_internacao = df.groupby('SP_CIDADE_H')['Duracao_Internacao'].mean().reset_index()
    media_internacao.columns = ['Município', 'Média de Dias de Internação']

    fig = px.bar(media_internacao, x='Município', y='Média de Dias de Internação',
        title='Média de Dias de Internação por Município',
        labels={'Município': 'Município do Hospital', 'Média de Dias de Internação': 'Média (em dias)'},
        color='Média de Dias de Internação',
        color_continuous_scale='Viridis')

    st.plotly_chart(fig)
