from .cached_data import merged_data, distritos, subprefeituras
from .merge_cadastro_ideb import JoinData


def get_data():
    """Atribui os dados mergidos a um DataFrame e retorna ele como df"""

    df = merged_data()

    return df


def get_distritos():
    """Atribui os dados dos distritos a um DataFrame e retorna ele como geodf"""

    geodf = distritos()

    return geodf


def get_subprefeituras():
    """Atribui os dados das subprefeituras a um DataFrame e retorna ele como geodf"""

    geodf = subprefeituras()

    return geodf
