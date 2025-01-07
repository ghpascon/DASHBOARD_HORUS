import pandas as pd
from datetime import datetime, date
import streamlit as st

def st_write(txt, font_size=20, sidebar = False):
    if not sidebar:
        st.markdown(f"<p style='font-size:{font_size}px;'>{txt}</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<p style='font-size:{font_size}px;'>{txt}</p>", unsafe_allow_html=True)

def get_interval(df, interval=None):
    if interval is None:
        return df
    return df[(df['date'] >= interval[0]) & (df['date'] <= interval[1])]

def get_interval_data(df,name):
    periodo_opcao = st.sidebar.radio('Selecione o periodo', ("Todo o período", "Hoje", "Este Mês", "Este Ano", "Intervalo personalizado"))

    # Resto da lógica permanece inalterada
    if periodo_opcao == "Todo o período":
        df_interval = get_interval(df)

    elif periodo_opcao == "Hoje":
        df_interval = get_interval(df, (date.today().strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')))

    elif periodo_opcao == "Este Mês":
        df_interval = get_interval(df, (date(date.today().year, date.today().month, 1).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')))

    elif periodo_opcao == "Este Ano":
        df_interval = get_interval(df, (date(date.today().year, 1, 1).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')))

    elif periodo_opcao == "Intervalo personalizado":
        data_inicial = st.sidebar.date_input("Data Inicial", datetime.today(), help="Selecione a data inicial", key="inicial")
        data_final = st.sidebar.date_input("Data Final", datetime.today(), help="Selecione a data final", key="final")

        if data_final < data_inicial:
            st.warning("A data final não pode ser anterior à data inicial.")
            return None
        else:
            df_interval = get_interval(df, (str(data_inicial), str(data_final)))

    st_write(f"Período selecionado: <b>{periodo_opcao}</b>",sidebar=False)
    if periodo_opcao == "Intervalo personalizado":
        st_write(f"Intervalo selecionado: {data_inicial} a {data_final}")

    return df_interval.reset_index(drop=True)