from .dados_cadastro_escola import DadosCadastroEscola
from .ideb_data import ideb_finais, ideb_iniciais
from .merge_cadastro_ideb import JoinData

def get_data(path='data', ano_cadastro=2019):

    pegar_cadastro = DadosCadastroEscola()
    cadastro = pegar_cadastro.dataframe_ano(ano_cadastro)

    iniciais = ideb_iniciais()
    finais = ideb_finais()

    join = JoinData()
    df = join(cadastro, iniciais, finais, path_salvar=path)

    return df