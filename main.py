import pandas as pd
import streamlit as st
from app import utils, images, st_utils, auth, mysql_utils, pages
    

if __name__ == '__main__':
    st.set_page_config(
        page_title="Dashboard Horus",
        page_icon="data/logo_horus.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    df = utils.get_data()
    df = utils.treat_df(df)
    df_interval = None

    st.image(st.secrets['logo']['logo'])

    name = auth.autenticacao()

    if name is not None:
        page = 'Visualização'
        if st.session_state['roles'] == ['admin']:
            page = st.sidebar.selectbox('Menu Admin', ("Visualização", "Usuários"))

        if page == 'Visualização':
            pages.page_visualizacao(df, name)  

        elif page == 'Usuários':
            pages.page_usuarios()      

    # streamlit run main.py    


