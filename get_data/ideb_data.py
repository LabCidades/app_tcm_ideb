import os
import pandas as pd
from .parse_ideb import DataIdebFinais, DataIdebIniciais

def download_df_salvo(path_salvo):
    
    if os.path.exists(path_salvo):
        df = pd.read_csv(path_salvo, sep=';')
        if "Unnamed: 0" in df:
            df.drop("Unnamed: 0",axis=1,inplace=True)
        return df
    return None

def ideb_finais():
    
    path_salvo = 'raw_data/ideb_parsed/dados_ideb_finais.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        return df
    
    finais = DataIdebFinais()
    finais.save_data()
    
    return finais.data

def ideb_iniciais():
    
    path_salvo = 'raw_data/ideb_parsed/dados_ideb_iniciais.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        return df
    
    iniciais = DataIdebIniciais()
    iniciais.save_data()
    
    return iniciais.data
        