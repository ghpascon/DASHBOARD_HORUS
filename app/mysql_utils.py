import streamlit as st

def get_users():
    conn = st.connection('mysql', type='sql')

    # Perform query.
    df = conn.query('SELECT * from users;')
    df = df.drop(columns=['idusers'])
    credentials = []
    for _, row in df.iterrows():
        credentials.append([col for col in row])

    return credentials


def add_user(name, username, password, email, role):
    try:
        # Conectar ao banco de dados
        conn = st.connection('mysql', type='sql')
        
        # Verificar se o username já existe
        check_query = f"SELECT COUNT(*) FROM users WHERE username = '{username}';"
        
        # Executar a consulta de verificação do username usando query
        result = conn.query(check_query)
        

        # Verificar se o username já existe
        if result.iloc[0, 0] > 0:  # Se o username já existe
            print(f'Usuario existente: {username}')
            st.error("O nome de usuário já está em uso. Escolha outro.")
            return  # Não prossegue se o username já existir

        # Preparar a query SQL para inserir os dados
        print(f'Adicionando {username}')
        insert_query = f"""
        INSERT INTO users (name, username, password, email, role)
        VALUES ('{name}', '{username}', '{password}', '{email}', '{role}');
        """

        # Executar a query de inserção com os dados fornecidos usando query
        conn.query(insert_query)
        
        # Confirmação de sucesso
        st.success("Usuário adicionado com sucesso!")

    except Exception as e:
        st.error(f"Falha ao adicionar um usuário: {str(e)}")