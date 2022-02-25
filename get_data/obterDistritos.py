import os
import pandas as pd
import geopandas as gpd
from json import dumps
import numpy as np


def distritos(path_salvo, dfIdebIniciais, dfIdebFinais):
    """Filtra os GeoDados dos distritos"""

    if os.path.exists(path_salvo):

        geodfDistritos = gpd.read_file(path_salvo)
        # geodfDistritos.to_file('c:\\c2\\myshpfile.geojson', driver='GeoJSON')

        if "Unnamed: 0" in geodfDistritos:
            geodfDistritos.drop("Unnamed: 0", axis=1, inplace=True)

        geodfDistritos.set_crs(epsg=31983, inplace=True)

    if geodfDistritos is not None:
        dfIdebIniciais['coddist'] = dfIdebIniciais['coddist'].astype(int).astype(str)
        geodfAgrupado = dfIdebIniciais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        dfU = dfIdebIniciais[['coddist', 'universalizacao_2019', 'universalizacao_2020']]
        dfU = dfU.copy()
        dfU['universalizacao_2019'] = pd.to_numeric(dfU['universalizacao_2019'], errors='coerce')
        dfU['universalizacao_2019'] = dfU['universalizacao_2019'].apply(
            lambda x: round(x, 2) if not pd.isnull(x) else 0)
        dfU['universalizacao_2020'] = pd.to_numeric(dfU['universalizacao_2020'], errors='coerce')
        dfU['universalizacao_2020'] = dfU['universalizacao_2020'].apply(
            lambda x: round(x, 2) if not pd.isnull(x) else 0)
        # dfU = dfU.replace(np.nan, 0, regex=True)

        # dfU = dfIdebIniciais[['A', 'C', 'D']].copy()
        # dfU['universalizacao_2019'] = dfU['universalizacao_2019'].astype(float)
        # dfU['universalizacao_2019'] = pd.to_numeric(dfU['universalizacao_2019'], errors='coerce')
        # dfU['universalizacao_2019'] = dfU['universalizacao_2019'].fillna(0)

        # dfU['universalizacao_2020'] = pd.to_numeric(dfU['universalizacao_2020'], errors='coerce')
        # dfU['universalizacao_2020'] = dfU['universalizacao_2020'].fillna(0)
        # dfU['universalizacao_2020'] = dfU['universalizacao_2020'].astype(float)
        dfU['universalizacao_2020'] = dfU['universalizacao_2020']
        dfU = dfU.drop_duplicates()
        dfU = dfU.sort_values('coddist')

        dfGastos = dfIdebIniciais[['coddist', 'gastos_2019', 'PER_CAPITA_anual_2020', 'REMUNERACAO_BRUTA']]
        dfGastos = dfGastos.copy()
        dfGastos['gastos_2019'] = pd.to_numeric(dfGastos['gastos_2019'], errors='coerce')
        dfGastos['gastos_2019'] = dfGastos['gastos_2019'].apply(
            lambda x: round(x, 2) if not pd.isnull(x) else 0)
        dfGastos['PER_CAPITA_anual_2020'] = pd.to_numeric(dfGastos['PER_CAPITA_anual_2020'], errors='coerce')
        dfGastos['PER_CAPITA_anual_2020'] = dfGastos['PER_CAPITA_anual_2020'].apply(
            lambda x: round(x, 2) if not pd.isnull(x) else 0)
        dfGastos['REMUNERACAO_BRUTA'] = dfGastos['REMUNERACAO_BRUTA'].str.replace(',', '.').astype(float)
        dfGastos['REMUNERACAO_BRUTA'] = pd.to_numeric(dfGastos['REMUNERACAO_BRUTA'], errors='coerce')
        dfGastos['REMUNERACAO_BRUTA'] = dfGastos['REMUNERACAO_BRUTA'].apply(
            lambda x: round(x, 2) if not pd.isnull(x) else 0)
        # dfGastos = dfGastos.replace(np.nan, 0, regex=True)
        dfGastos = dfGastos.drop_duplicates()
        dfGastos = dfGastos.sort_values('coddist')

        dfMerged = pd.merge(geodfDistritos, geodfAgrupado,
                            how='left', left_on='ds_codigo', right_on='coddist')

        # ds = dfMerged[dfMerged.columns[0:5]]
        # ds.to_excel("c:\\c2\\ds.xlsx")

        dfIdebFinais['coddist'] = dfIdebFinais['coddist'].astype(int).astype(str)
        geodfAgrupado = dfIdebFinais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        dfMerged2 = pd.merge(dfMerged, geodfAgrupado,
                             how='left', left_on='ds_codigo', right_on='coddist')

        dfMerged2 = dfMerged2.rename(columns={'ideb_2019_x': 'ideb_iniciais', 'ideb_2019_y': 'ideb_finais'})
        dfMerged2['ideb_iniciais'] = dfMerged2['ideb_iniciais'].fillna(0)
        dfMerged2['ideb_finais'] = dfMerged2['ideb_finais'].fillna(0)
        media = dfMerged2['ideb_iniciais'] + dfMerged2['ideb_finais']
        dfMerged2['media_final'] = media / 2

        geodfAgrupadox = dfIdebFinais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].min()

        dfMerged2 = pd.merge(dfMerged2, dfU,
                             how='left', left_on='ds_codigo', right_on='coddist')

        dfMerged2 = pd.merge(dfMerged2, dfGastos,
                             how='left', left_on='ds_codigo', right_on='coddist')

        dfMerged2['universalizacao_2019'] = dfMerged2['universalizacao_2019'].fillna(0)
        dfMerged2['universalizacao_2020'] = dfMerged2['universalizacao_2020'].fillna(0)

    return dfMerged2
