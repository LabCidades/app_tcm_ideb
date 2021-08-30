import pandas as pd
from get_data import distritos_shp, get_data, get_distritos

class RegionalizarDistritos:


    def agrupar_distritos_media(self, microdados_ideb):

        grouped = microdados_ideb.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        return grouped

    def filtrar_tipo_anos(self, grouped, tipo_anos):

        if tipo_anos not in ('finais', 'iniciais'):
            raise ValueError(f'Tipo de anos {tipo_anos} não existente')

        df_anos = grouped.loc[tipo_anos].reset_index() 

        return df_anos

    def padronizar_codigo_distrito_ideb(self, df_anos):

        df_anos['coddist'] = df_anos['coddist'].astype(int).astype(str)

        return df_anos

    def merge_shapefile(self, df_anos, distritos):

        df_anos = self.padronizar_codigo_distrito_ideb(df_anos)

        merged = pd.merge(distritos, df_anos, 
                    how='left', left_on='ds_codigo', right_on='coddist')

        return merged

    

    def __call__(self, tipo_anos, microdados_ideb=None, distritos=None):

        if tipo_anos not in ('finais', 'iniciais'):
            raise ValueError(f'Tipo de anos {tipo_anos} não existente')

        if microdados_ideb is None:
            microdados_ideb = get_data()
        
        if distritos is None:
            distritos = get_distritos()

        grouped = self.agrupar_distritos_media(microdados_ideb)
        df_anos = self.filtrar_tipo_anos(grouped, tipo_anos=tipo_anos)

        return self.merge_shapefile(df_anos, distritos)


    