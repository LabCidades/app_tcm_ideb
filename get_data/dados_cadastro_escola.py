from io import StringIO
import pandas as pd
import os
from .dados_abertos import DadosAbertos

class DadosCadastroEscola:
    
    url = ('http://dados.prefeitura.sp.gov.br/pt_PT/'
            'dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas')
    extensoes= ('csv',)

    path_salvar =  'raw_data/cadastro_2019/'
    
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

    def salvar_dados(self, df, sep, save_path = None):

        if save_path is None:
            save_path = self.path_salvar

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        file_name = os.path.join(save_path, 'cadastro_2019.csv')

        df.to_csv(file_name, sep=sep, index=False)
        print('Dados cadastrais salvos com sucesso')
            
    def dataframe_ano(self, ano, sep = ';', save_data=True):
        
        download = self.baixar_cadastro_ano(ano)
        
        df = pd.read_csv(StringIO(download), sep=sep)

        if save_data:
            self.salvar_dados(df, sep)
        
        return df



        