import os
import pandas as pd


def dadosIdeb(path_salvo):
    """Lê os dados do ideb de acordo com o path_salvo"""

    if os.path.exists(path_salvo):
        df = pd.read_csv(path_salvo, encoding='latin-1', sep=';')
        if "Unnamed: 0" in df:
            df.drop("Unnamed: 0", axis=1, inplace=True)

    if df is not None:
        print('Dados Ideb carregados.')

    return df
