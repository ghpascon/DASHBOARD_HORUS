import streamlit as st
import streamlit_authenticator as stauth
from app import mysql_utils


def autenticacao():
    users_data = mysql_utils.get_users()
    print(users_data)
    # Cria a estrutura de credenciais do streamlit-authenticator
    credentials_dict = {
        "usernames": {
            st.secrets['master']['username']: {
                "name": st.secrets['master']['name'],
                "password": st.secrets['master']['password'],
                "email": st.secrets['master']['email'],
                "roles": ["admin"],
            }
        }
    }

    # # # Adiciona outros usuários da base de dados
    for user in users_data:
        username = user[1]
        credentials_dict["usernames"][username] = {
            "name": user[0],
            "password": user[2],
            "email": user[3],
            "roles": user[4],  # Define a role como "user" para usuários normais
        }

    # Configura o autenticador
    authenticator = stauth.Authenticate(
        credentials=credentials_dict,
        cookie_name=st.secrets['cookie']['name'],
        key="my_signature_key",
        cookie_expiry_days=30,
    )

    # Função de login
    def login():
        # name, authentication_status, username = 
        authenticator.login(
            "main",
            fields={"username": "Username", "password": "Password", "Login": "Entrar"},
            clear_on_submit=True,
        )
        return st.session_state["name"], st.session_state['authentication_status']

    # Função de logout
    def logout(name):
        st.sidebar.write(f"Logado como: {name}")
        authenticator.logout("Logout", "sidebar")

    # Fluxo principal de autenticação
    name, authentication_status = login()

    if authentication_status:
        logout(name)
        return name  # Retorna o nome do usuário autenticado
    elif authentication_status is False:
        st.error("Nome de usuário ou senha incorretos.")
    elif authentication_status is None:
        st.warning("Por favor, insira seu nome de usuário e senha.")

    return None  # Retorna None se a autenticação não for bem-sucedida
