import pandas as pd
import numpy as np
import os


class IdebCleaner:

    def nan_col_ideb(self, df):

        col_ideb = 'ideb_2019'

        df[col_ideb] = df[col_ideb].apply(lambda x: np.NaN if x == '-' else x)

        return df

    def filtrar_rede_municipal(self, df):

        filtro = df['tipo_rede'] == 'Municipal'

        return df[filtro].copy().reset_index(drop=True)

    def filtrar_municipio_sp(self, df):

        codigo_sampa = 3550308
        filtro = df['codigo_municipio'] == codigo_sampa

        return df[filtro].copy().reset_index(drop=True)
    
    def drop_ideb_cols(self, df):
        
        dropar = ['codigo_municipio', 'tipo_rede']
        
        df = df.drop(dropar, axis=1).copy()
        
        return df
    
    def codigo_to_str(self, df):
        
        df['codigo_escola'] = df['codigo_escola'].astype(str)
        
        return df

    def clean_ideb(self, df):

        df = self.nan_col_ideb(df)
        df = self.filtrar_rede_municipal(df)
        df = self.filtrar_municipio_sp(df)
        df = self.drop_ideb_cols(df)
        df = self.codigo_to_str(df)
        
        return df
    
    def __call__(self, df):
        
        return self.clean_ideb(df)


class CadastroCleaner:
    
    def limpar_codinep(self, cadastro):
        
        func = lambda x: str(int(x)) if not pd.isnull(x) else x
        
        cadastro['codinep'] = cadastro['codinep'].apply(func)
        
        return cadastro
    
    def filtrar_codinep_vazio(self, cadastro):
        
        filtro = cadastro['codinep'].isnull()
        
        return cadastro[~filtro].reset_index(drop=True)
    
    def drop_cadastro_cols(self, cadastro):
        
        cols_uteis = ['codinep', 'tipoesc', 'nomesc', 
                      'subpref', 'coddist']
        
        cadastro = cadastro[cols_uteis].copy()
        
        return cadastro

    def __call__(self, cadastro):
        
        cadastro = self.limpar_codinep(cadastro)
        cadastro = self.filtrar_codinep_vazio(cadastro)
        cadastro = self.drop_cadastro_cols(cadastro)
        
        return cadastro
    

class JoinData:
    
    def __init__(self):
        
        self.clean_ideb = IdebCleaner()
        self.clean_cadastro = CadastroCleaner()

    def clean_data(self, cadastro, ideb_inicias, ideb_finais):
        """Limpa os dados de cadastro ideb_inicias e ideb_finais"""
        
        ideb_inicias = self.clean_ideb(ideb_inicias)
        ideb_finais = self.clean_ideb(ideb_finais)
        cadastro = self.clean_cadastro(cadastro)
        
        return cadastro, ideb_inicias, ideb_finais
        
    def join_ideb(self, ideb_iniciais, ideb_finais):
        """Faz o join do ideb iniciais com o finais e retorna o joined"""
        
        joined = pd.concat([ideb_iniciais, ideb_finais])
        # for some reason it's casting int when joining
        joined['codigo_escola'] = joined['codigo_escola'].astype(str)
        
        return joined
    
    def merge_ideb_cadastro(self, ideb_geral, cadastro):
        """Faz o merge do ideb geral com cadastro e retorna o merged"""

        merged = pd.merge(ideb_geral, cadastro, 
                          how='left', left_on='codigo_escola', 
                          right_on='codinep')
        
        return merged

    def save_joined_df(self, df, path='data'):
        """Salva caminho dos dados mergidos em cadastro_ideb_merged.csv"""

        if not os.path.exists(path):
            os.mkdir(path)
        
        df.to_csv(os.path.join(path, 'cadastro_ideb_merged.csv'), index=False,
                  sep=';')
        print('Dados merged ideb e cadastrais salvos com sucesso')
    
    def __call__(self, cadastro, ideb_inicias, ideb_finais, path_salvar=None):
        """Chama a si mesmo, relizando a limpeza, join e merge de cadastro, ideb_inicias e ideb_finais"""
        
        cadastro, iniciais, finais = self.clean_data(
                                                    cadastro, 
                                                    ideb_inicias, 
                                                    ideb_finais)
        ideb = self.join_ideb(iniciais, finais)
        merged = self.merge_ideb_cadastro(ideb, cadastro)

        if path_salvar is not None:
            self.save_joined_df(merged, path_salvar)
        
        return merged
