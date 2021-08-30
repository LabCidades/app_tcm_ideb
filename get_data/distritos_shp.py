import requests
import os
from zipfile import ZipFile
from io import BytesIO
import geopandas as gpd

class DownloadShapeDists:
    
    url_distritos = ('http://download.geosampa.prefeitura.sp.gov.br/PaginasPublicas/'
                'downloadArquivo.aspx?orig=DownloadCamadas&'
                'arq=01_Limites%20Administrativos%5C%5CDistrito%5C%5CShapefile%5C%5CSIRGAS_SHP_distrito&arqTipo=Shapefile')
    
    path_dados = 'data/geo_data'
    
    def download(self):
        
        with requests.get(self.url_distritos) as r:
            shape_zip = r.content
        return shape_zip
    
    def solve_data_dir(self, data_dir=None):
        
        if data_dir is None:
            data_dir = self.path_dados
            
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        return data_dir
    
    def unzip(self, shape_zip, path_dados=None):
                
        zip_file = ZipFile(BytesIO(shape_zip))
        path_dados = self.solve_data_dir(path_dados)
        
        zip_file.extractall(path_dados)

    def open_shape(self, path_dados=None):

        path_dados = self.solve_data_dir(path_dados)
        path_file = os.path.join(path_dados, 'SIRGAS_SHP_distrito/SIRGAS_SHP_distrito_polygon.shp')

        geodf = gpd.read_file(path_file)

        geodf.set_crs(epsg = 31983, inplace=True)

        return geodf
        
    def __call__(self):
        
        shape_zip = self.download()
        
        self.unzip(shape_zip)
        print("Shape distritos baixado e salvado com sucesso")

        geodf = self.open_shape()
        
        return geodf