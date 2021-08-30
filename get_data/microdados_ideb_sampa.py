from .cached_data import ideb_finais, ideb_iniciais, cadastro_2019
from .merge_cadastro_ideb import JoinData

def get_data(path='data', ano_cadastro=2019):

    

    iniciais = ideb_iniciais()
    finais = ideb_finais()
    cadastro = cadastro_2019()
    join = JoinData()
    df = join(cadastro, iniciais, finais, path_salvar=path)

    return df