import pandas as pd
import streamlit as st
from app import  images, st_utils, mysql_utils

def page_visualizacao(df, name):    
    st_utils.st_write(f'Bem vindo {name}', 50)

    df_interval = st_utils.get_interval_data(df, name)
    if df_interval is not None:
        st.divider()

        labels = ['ATENDIDA', 'NA', 'ENDCALL']
        colors = ['#ffffff', '#00ff00', '#ff0000', '#cccccc']
        images.generate_boxes(list(df_interval['status']), labels, colors, 200, 200)

        st.divider()

        st.table(df_interval)

def page_usuarios():
    # Criando as abas (tabs)
    tabs = st.tabs(["Adicionar Usuário", "Selecionar Usuário"])

    with tabs[0]:
        # Selecione "Adicionar Usuário", exibe o formulário de adição de usuário
        st.header("Adicionar Novo Usuário")
        with st.form(key="add_user_form"):
            name = st.text_input("Nome Completo")
            username = st.text_input("Username")
            password = st.text_input("Senha", type="password")
            email = st.text_input("Email")
            role = st.selectbox("Selecione o Role", ["admin", "user"])

            submit_button = st.form_submit_button(label="Adicionar Usuário")
            
            if submit_button:
                # Adiciona o usuário no banco de dados
                mysql_utils.add_user(name, username, password, email, role)

    with tabs[1]:
        # Selecione "Selecionar Usuário", exibe a tabela de usuários
        st.header("Selecione um Usuário")
        
        # Recupera dados dos usuários do banco de dados
        user_data = mysql_utils.get_users()

        # Exibe a tabela com os dados dos usuários
        st.table(user_data)

        # Permite ao usuário selecionar um usuário da lista
        usernames = [user[1] for user in user_data]  # Supondo que o username seja a segunda coluna
        selected_username = st.selectbox("Selecione um usuário", usernames)

        # Encontre o usuário selecionado no banco de dados
        selected_user = None
        for user in user_data:
            if user[1] == selected_username:  # Comparando pelo nome de usuário
                selected_user = user
                break

        # Se um usuário for selecionado, exibe suas informações
        if selected_user:
            st.write(f"Informações do usuário:")
            st.write(f"Nome: {selected_user[0]}")
            st.write(f"Username: {selected_user[1]}")
            st.write(f"Email: {selected_user[3]}")
            st.write(f"Role: {selected_user[4]}")
            # Você pode adicionar mais detalhes conforme a estrutura da sua tabela

        else:
            st.write("Nenhum usuário selecionado.")