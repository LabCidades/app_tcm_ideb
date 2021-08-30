from .cached_data import merged_data
from .merge_cadastro_ideb import JoinData

def get_data(path='data', ano_cadastro=2019):

    df = merged_data()

    return df