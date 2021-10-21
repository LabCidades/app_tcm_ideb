import os
import pandas as pd
import geopandas as gpd
from .dados_cadastro_escola import DadosCadastroEscola
from .parse_ideb import DataIdebFinais, DataIdebIniciais
from .merge_cadastro_ideb import JoinData
from .distritos_shp import DownloadShapeDists

def download_df_salvo(path_salvo):
    
    if os.path.exists(path_salvo):
        df = pd.read_csv(path_salvo, sep=';')
        if "Unnamed: 0" in df:
            df.drop("Unnamed: 0",axis=1,inplace=True)
        return df
    return None

def download_shape_salvo(path_salvo, epsg):

    if os.path.exists(path_salvo):
        geodf = gpd.read_file(path_salvo)
        if "Unnamed: 0" in geodf:
            geodf.drop("Unnamed: 0",axis=1,inplace=True)
        geodf.set_crs(epsg = epsg, inplace=True)
        return geodf
    return None


def ideb_finais():
    
    path_salvo = 'raw_data/ideb_parsed/dados_ideb_finais.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        print('Ideb finais cacheado.')
        return df
    
    finais = DataIdebFinais()
    finais.save_data()
    
    return finais.data

def ideb_iniciais():
    
    path_salvo = 'raw_data/ideb_parsed/dados_ideb_iniciais.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        print('Ideb inicias cacheado.')
        return df
    
    iniciais = DataIdebIniciais()
    iniciais.save_data()
    
    return iniciais.data

def cadastro_2019():

    path_salvo = 'raw_data/cadastro_2019/cadastro_2019.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        print('Dados cadastro 2019 cacheados.')
        return df
    
    pegar_cadastro = DadosCadastroEscola()
    cadastro_2019 = pegar_cadastro.dataframe_ano(2019)
    
    return cadastro_2019 

def merged_data():

    path_salvo = 'data/cadastro_ideb_merged.csv'
    df = download_df_salvo(path_salvo)
    if df is not None:
        print('Dados merged cacheados.')
        return df
    
    iniciais = ideb_iniciais()
    finais = ideb_finais()
    cadastro = cadastro_2019()

    join = JoinData()
    df = join(cadastro, iniciais, finais, path_salvar='data')

    return df

def distritos():

    path_salvo = 'data/geo_data/SIRGAS_SHP_distrito'
    geodf = download_shape_salvo(path_salvo, 31983)
    if geodf is not None:
        print('Dados distrito shape cacheados.')
        return geodf

    download_distritos = DownloadShapeDists()
    geodf = download_distritos()

    return geodf

def subprefeituras():

    path_salvo = 'data/geo_data/SIRGAS_SHP_subprefeitura'
    geodf = download_shape_salvo(path_salvo, 31983)

    if geodf is not None:
        print('Dados Subprefeituras shape cacheados.')
        return geodf

    download_distritos = DownloadShapeDists()
    geodf = download_distritos()

    return geodf

    