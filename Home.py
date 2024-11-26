#importa as bib
import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#layout="wide" -> pagina pega mais da tela (senao fica muito apertado)
#page_title -> titulo da pagina (nome que o Tab da pagina vai ter)
st.set_page_config(page_title="Compilado de Gráficos", layout="wide")

with st.container():
    st.subheader("Página Inicial")
    st.title('Compilado de Gráficos')
    st.write('Esta página StreamLit foi criada com o intuito de agrupar os gráficos gerados pelo grupo 1 da disciplina Prática em Pesquisa, escolha o tipo de gráfico que deseja ver, ao lado esquerdo')
    #st.write('write e [link](https://pt.wikipedia.org/wiki/Wikipédia:Página_principal)')