import os
import pandas as pd
import geopandas as gpd


def subprefeituras(path_salvo, dfIdebIniciais, dfIdebFinais):
    """Filtra os GeoDados das subprefeituras"""

    if os.path.exists(path_salvo):

        geodfSubprefeituras = gpd.read_file(path_salvo)

        if "Unnamed: 0" in geodfSubprefeituras:
            geodfSubprefeituras.drop("Unnamed: 0", axis=1, inplace=True)

        geodfSubprefeituras.set_crs(epsg=31983, inplace=True)

    if geodfSubprefeituras is not None:

        dfIdebIniciais['codsub'] = dfIdebIniciais['codsub'].astype(int).astype(str)
        geodfAgrupado = dfIdebIniciais.groupby(['tipo_anos', 'codsub'])[['ideb_2019']].mean()

        geodfSubprefeituras['sp_id'] = geodfSubprefeituras['sp_id'].astype(int).astype(str)

        dfMerged = pd.merge(geodfSubprefeituras, geodfAgrupado,
                            how='left', left_on='sp_id', right_on='codsub')

        dfIdebFinais['codsub'] = dfIdebFinais['codsub'].astype(int).astype(str)
        geodfAgrupado = dfIdebFinais.groupby(['tipo_anos', 'codsub'])[['ideb_2019']].mean()

        dfMerged2 = pd.merge(dfMerged, geodfAgrupado,
                             how='left', left_on='sp_id', right_on='codsub')

        dfMerged2 = dfMerged2.rename(columns={'ideb_2019_x': 'ideb_iniciais', 'ideb_2019_y': 'ideb_finais'})
        dfMerged2['ideb_iniciais'] = dfMerged2['ideb_iniciais'].fillna(0)
        dfMerged2['ideb_finais'] = dfMerged2['ideb_finais'].fillna(0)
        media = dfMerged2['ideb_iniciais'] + dfMerged2['ideb_finais']
        dfMerged2['media_final'] = media / 2

        print('Dados Subprefeituras carregados.')

    return dfMerged2
