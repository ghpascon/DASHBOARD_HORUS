import json
import pandas as pd
import pytz


def get_df(cdr_log):
    df_data = []

    for line in cdr_log:
        data_features = line.split(',')
        df_data.append(data_features)

    return pd.DataFrame(df_data)

def get_data(path):
    with open(path, "r", encoding="utf-8") as json_file:
        config = json.load(json_file)  # Carrega o JSON como um dicionário
        file_path = config['cdr_path']

    cdr_log = []
    with open(file_path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha != '\n': cdr_log.append(linha)

    return get_df(cdr_log)

def treat_df(df_raw):
    #DATE
    date = pd.to_datetime(df_raw[3])
    original_timezone = pytz.utc
    br_timezone = pytz.timezone('America/Sao_Paulo')
    date_br = [dat.replace(tzinfo=original_timezone).astimezone(br_timezone) for dat in date]

    #DURACAO
    duracao = df_raw[2].copy().replace('','NULL')

    #CHAIN
    chain = []
    for call in df_raw[20]:
        if call is None: 
            chain.append('-')
            continue
        call = call.replace('Chain:','')
        chain.append(call)

    #CHAIN_END
    chain_end = [call.split(';')[-2 if len(call) > 1 else -1] for call in chain]

    #TERMINATED
    terminated = df_raw[7].copy()

    #STATUS
    status = []
    for sts in chain_end:
        if sts == '-':
            status.append('ERRO')
        elif sts.startswith('Ext.8'):
            status.append('NA')
        elif sts == 'EndCall': 
            status.append('ENDCALL')
        else:
            status.append('ATENDIDA')

    #DF
    df = pd.DataFrame()
    df['date'] = date_br
    df['duration'] = duracao
    df['chain'] = chain
    df['chain_end'] = chain_end
    df['terminated'] = terminated
    df['status'] = status
    return df
