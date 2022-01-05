import pandas as pd
import get_data as gpd
from get_data import get_data, get_distritos, get_subprefeituras


class RegionalizarDistritos:

    def agrupar_distritos_media(self, microdados_ideb):
        """(Possivelmente obsoleta) Agrupando os dados dos distritos através da média,
        retornando um dataframe grouped"""

        grouped = microdados_ideb.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        return grouped

    def agrupar_subprefeituras_media(self, microdados_ideb):
        """(Possivelmente obsoleta) Agrupando os dados das subprefeituras através da média
        retornando um dataframe grouped"""

        grouped = microdados_ideb.groupby(['tipo_anos', 'codsub'])[['ideb_2019']].mean()

        return grouped

    def filtrar_tipo_anos(self, grouped, tipo_anos):
        """(Possivelmente obsoleta) fazendo a filtragem de dados de acordo com o tipo de anos (iniciais ou finais)
        retornando um dataframe df_anos"""


        if tipo_anos not in ('finais', 'iniciais'):
            raise ValueError(f'Tipo de anos {tipo_anos} não existente')

        df_anos = grouped.loc[tipo_anos].reset_index() 

        return df_anos

    def padronizar_codigo_distrito_ideb(self, df_anos):
        """Padronizando os distritos do df_anos de acordo com o código do distrito"""

        df_anos['coddist'] = df_anos['coddist'].astype(int).astype(str)

        df_anos.to_csv("df_anos.csv")

        return df_anos

    def padronizar_codigo_subprefeitura_ideb(self, df_anos):
        """Padronizando as subprefeituras do df_anos de acordo com o código da subprefeitura"""

        df_anos['codsub'] = df_anos['codsub'].astype(int).astype(str)

        df_anos.to_csv("df_anos.csv")

        return df_anos

    def merge_shapefile(self, df_anos, distritos):
        """Fazendo merge dos DataFrames distritos e df_anos através de seus códigos"""

        df_anos = self.padronizar_codigo_distrito_ideb(df_anos)

        merged = pd.merge(distritos, df_anos, 
                          how='left', left_on='ds_codigo', right_on='coddist')

        return merged

    def merge_shapefile_sub(self, df_anos, subprefeituras):
        """Fazendo merge dos DataFrames subprefeituras e df_anos através de seus códigos"""

        df_anos = self.padronizar_codigo_subprefeitura_ideb(df_anos)

        merged = pd.merge(subprefeituras, df_anos,
                          how='left', left_on='sp_id', right_on='codsub')

        return merged

    def __call__(self, tipo_anos, microdados_ideb=None, distritos=None, subprefeituras=None):
        """Agrupando os dados para mergir o shapefile"""

        if tipo_anos not in ('finais', 'iniciais'):
            raise ValueError(f'Tipo de anos {tipo_anos} não existente')

        if microdados_ideb is None:
            microdados_ideb = get_data()

        if distritos is None:
            distritos = get_distritos()

        if subprefeituras is None:
            subprefeituras = get_subprefeituras()

        grouped = self.agrupar_distritos_media(microdados_ideb)
        df_anos = self.filtrar_tipo_anos(grouped, tipo_anos=tipo_anos)

        grouped = self.agrupar_subprefeituras_media(microdados_ideb)
        df_anos = self.filtrar_tipo_anos(grouped, tipo_anos=tipo_anos)

        dfs = self.merge_shapefile_sub(df_anos, subprefeituras)
        self.geodfSubprefeituras = dfs

        return self.merge_shapefile(df_anos, distritos)


    