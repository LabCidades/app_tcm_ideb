import pandas as pd
import get_data as gpd
from get_data import get_data, get_distritos, get_subprefeituras


class RegionalizarDistritos:

    def agrupar_distritos_media(self, microdados_ideb):

        grouped = microdados_ideb.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        return grouped

    def agrupar_subprefeituras_media(self, microdados_ideb):

        grouped = microdados_ideb.groupby(['tipo_anos', 'codsub'])[['ideb_2019']].mean()

        return grouped

    def filtrar_tipo_anos(self, grouped, tipo_anos):

        if tipo_anos not in ('finais', 'iniciais'):
            raise ValueError(f'Tipo de anos {tipo_anos} não existente')

        df_anos = grouped.loc[tipo_anos].reset_index() 

        return df_anos

    def padronizar_codigo_distrito_ideb(self, df_anos):

        df_anos['coddist'] = df_anos['coddist'].astype(int).astype(str)

        df_anos.to_csv("df_anos.csv")

        return df_anos

    def padronizar_codigo_subprefeitura_ideb(self, df_anos):

        df_anos['codsub'] = df_anos['codsub'].astype(int).astype(str)

        df_anos.to_csv("df_anos.csv")

        return df_anos

    def merge_shapefile(self, df_anos, distritos):

        df_anos = self.padronizar_codigo_distrito_ideb(df_anos)

        merged = pd.merge(distritos, df_anos, 
                          how='left', left_on='ds_codigo', right_on='coddist')

        return merged

    def merge_shapefile_sub(self, df_anos, subprefeituras):

        df_anos = self.padronizar_codigo_subprefeitura_ideb(df_anos)

        merged = pd.merge(subprefeituras, df_anos,
                          how='left', left_on='sp_id', right_on='codsub')

        return merged

    def __call__(self, tipo_anos, microdados_ideb=None, distritos=None, subprefeituras=None):

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


    