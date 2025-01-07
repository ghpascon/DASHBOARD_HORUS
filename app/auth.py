import streamlit as st
import streamlit_authenticator as stauth
def autenticacao():
    # Dados de usuário e senha
    usernames = ['usuario1', 'usuario2']
    passwords = ['senha123', 'senha456']
    names = ['João', 'Maria']

    # Gerando hashes das senhas
    hashed_passwords = stauth.Hasher(passwords).generate()
    credentials = {
        "usernames": {
            usernames[0]: {
                "name": names[0],
                "password": hashed_passwords[0]
            },
            usernames[1]: {
                "name": names[1],
                "password": hashed_passwords[1]
            }
        }
    }

    # Configuração do autenticador
    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name="my_cookie", 
        key="my_signature_key", 
        cookie_expiry_days=30
    )

    
    # Função para exibir a página de login
    def login():
        # Mostrando o formulário de login
        name, authentication_status, username = authenticator.login('main',fields={'username': 'Username', 'password': 'Password', 'Login':'Entrar'})
        
        # Verificando se o login foi bem-sucedido
        if authentication_status:
            # st.success(f'Bem-vindo {name}!')
            return True,name
        elif authentication_status is False:
            st.error('Nome de usuário ou senha incorretos.')
        return False,None

    # Exibindo conteúdo protegido ou página de login
    login_sts, name_logged_in = login()
    if login_sts:
        return name_logged_in, authenticator
    else:
        st.stop() 

def logout(authenticator, name):
    st.sidebar.write('Logado: ' + name)
    if st.sidebar.button('Logout'):
        st.cache_data.clear()
        st.cache_resource.clear()
        authenticator._implement_logout()
        st.rerun()    
