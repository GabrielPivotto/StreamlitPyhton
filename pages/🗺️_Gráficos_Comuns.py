#importa as bib
import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import geopandas as gpd
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
    default_value = "Ordenar por Tempo Médio"

    choices = ["Ordenar por Tempo Médio", "Ordenar por Procedimento mais Comum"]
    selected = st.selectbox("Escolha uma opção", choices, index=choices.index(default_value))

    if(selected == "Ordenar por Tempo Médio"):
        dados = load_data()
        dados['TEMPO_DT'] = dados['SP_DTSAIDA'] - dados['SP_DTINTER']

        agrupa = dados.groupby('SP_N_PROC').agg(
            QTD = ('SP_QT_PROC', 'sum'),
            MEDIA_DT = ('TEMPO_DT', 'mean')
        )

        ordenado = agrupa.sort_values(by= 'MEDIA_DT', ascending = False)

        fig = px.bar(agrupa, y=agrupa.index, x='MEDIA_DT', barmode = 'group', color = 'MEDIA_DT', title="Procedimentos Com Maior Tempo Médio de Internação").update_layout(
            xaxis_title="Tempo Médio de Internação", 
            yaxis_title="Nome do Procedimento",
            yaxis={'categoryorder': 'total ascending'},
            height=650,
            width=1150
        )

        st.plotly_chart(fig)

    if(selected == "Ordenar por Procedimento mais Comum"):
        dados = load_data()
        dados['TEMPO_DT'] = dados['SP_DTSAIDA'] - dados['SP_DTINTER']
        
        agrupa = dados.groupby('SP_N_PROC').agg(
            QTD = ('SP_QT_PROC', 'sum'),
            MEDIA_DT = ('TEMPO_DT', 'mean')
        )
        
        ordem = agrupa.sort_values('QTD')
        print(ordem)
        
        fig = px.bar(ordem, y=ordem.index, x='MEDIA_DT', color = 'MEDIA_DT' ,barmode = 'group', title="Procedimentos Com Maior Tempo Médio de Internação").update_layout(
            xaxis_title="Tempo Médio de Internação", 
            yaxis_title="Nome do Procedimento",
            #yaxis={'categoryorder': 'total ascending'},
            height=650,
            width=1150
        )

        st.plotly_chart(fig)







with st.container():
    dados = load_data()
    st.write("---")

    dados['TEMPO_DT'] = dados['SP_DTSAIDA'] - dados['SP_DTINTER']

    agrupa = dados.groupby('SP_N_PROC').agg(
    QTD = ('SP_QT_PROC', 'sum'),
    MEDIA_DT = ('TEMPO_DT', 'mean')
    )

    fig = px.bar(agrupa, x=agrupa.index, y='QTD',
                 title='Frequência dos Procedimentos Realizados',
                 color='QTD').update_layout(
                    xaxis_title="Nome do Procedimento", 
                    yaxis_title="Quantidade",
                    xaxis={'categoryorder': 'total descending'},
                    height=1000)
    
    st.plotly_chart(fig)





with st.container():
    df = load_data()
    st.write("---")
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






with st.container():
    st.write("---")

    df = load_data()
    df['SP_DTINTER'] = pd.to_datetime(df['SP_DTINTER'], format='%Y%m%d')
    df = df[(df['SP_DTINTER'].dt.month == 8) & (df['SP_DTINTER'].dt.year == 2023)]

    agrupa = df.groupby(['SP_DTINTER']).agg(
        SOMA = ('SP_QT_PROC', 'sum')
    )

    # Gerar dados de exemplo
    mes = 8  # Novembro
    ano = 2023
    dias_no_mes = pd.date_range(f'{ano}-{mes}-01', f'{ano}-{mes}-28', freq='D')
    valores = np.random.randint(0, 100, len(dias_no_mes))

    # Criar um DataFrame
    df = pd.DataFrame({'Data': agrupa.index, 'Valor': agrupa.SOMA})

    # Adicionar informações auxiliares
    df['Dia_da_Semana'] = df['Data'].dt.dayofweek  # Segunda=0, Domingo=6
    df['Semana'] = df['Data'].dt.isocalendar().week - df['Data'].dt.isocalendar().week.min()

    # Criar a matriz para o heatmap
    heatmap_data = df.pivot(index='Semana', columns='Dia_da_Semana', values='Valor')

    # Criar o gráfico
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
        y=heatmap_data.index,
        colorscale='Viridis',
        colorbar_title="Valor"
    ))

    # Ajustar a ordem do eixo Y para crescente
    fig.update_layout(
        title=f"Distribuição de Procedimentos Totais por Dia - {mes}/{ano}",
        xaxis_title="Dia da Semana",
        yaxis_title="Semanas do Mês",
        yaxis=dict(
            tickmode='array',
            tickvals=heatmap_data.index,
            ticktext=[f"Semana {i}" for i in heatmap_data.index],
            autorange="reversed"  # Reverte a ordem padrão do eixo Y
        )
    )

    st.plotly_chart(fig)
