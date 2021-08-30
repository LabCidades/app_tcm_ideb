from .cached_data import merged_data, distritos
from .merge_cadastro_ideb import JoinData

def get_data():

    df = merged_data()

    return df

def get_distritos():

    geodf = distritos()

    return geodf