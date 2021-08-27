from io import StringIO
import pandas as pd
from .dados_abertos import DadosAbertos

class DadosCadastroEscola:
    
    url = ('http://dados.prefeitura.sp.gov.br/pt_PT/'
            'dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas')
    extensoes= ('csv',)
    
    def __init__(self):
        
        self.dados_abertos_client = DadosAbertos(self.url, self.extensoes)
    
    def parse_ano_rec(self, recurso):
        
        ano_rec = recurso['descricao'].split('/')[-1].strip('.,')
        
        return ano_rec
    
    def baixar_cadastro_ano(self, ano):
    
        recursos_disponiveis =  self.dados_abertos_client.recursos
        for rec in recursos_disponiveis:
            ano_rec = self.parse_ano_rec(rec)
            if int(ano_rec) == ano:
                print('Baixando recurso:')
                print(rec)
                return self.dados_abertos_client.get_content(rec)
        else:
            raise ValueError(f'Ano de cadastro {ano} não encontrado')
            
    def dataframe_ano(self, ano, sep = ';'):
        
        download = self.baixar_cadastro_ano(ano)
        
        return pd.read_csv(StringIO(download), sep=sep)