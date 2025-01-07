import pandas as pd
import streamlit as st
from app import utils, images, st_utils, auth

if __name__ == '__main__':
    df = utils.get_data('app/config.json')
    df = utils.treat_df(df)
    df_interval = None

    st.set_page_config(
        page_title="Dashboard Horus",  # Título da página
        page_icon="data/logo_horus.png",       # Ícone da página (pode usar emoji ou caminho para imagem)
        layout="wide",                 # Layout da página (pode ser "centered" ou "wide")
        initial_sidebar_state="expanded"  # Estado inicial da barra lateral (pode ser "auto", "expanded", ou "collapsed")
    )

    st.image('data/logo_horus.png')

    name, authenticator = auth.autenticacao()

    auth.logout(authenticator, name)
    
    st_utils.st_write(f'Bem vindo {name}', 50)

    df_interval = st_utils.get_interval_data(df, name)
    if df_interval is not None:
        st.divider()

        labels = ['ATENDIDA', 'NA', 'ENDCALL']
        colors = ['#ffffff', '#00ff00', '#ff0000', '#cccccc']
        images.generate_boxes(list(df_interval['status']), labels, colors, 200, 200)

        st.divider()

        st.table(df_interval)
        
# streamlit run main.py    


