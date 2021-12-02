import requests
from zipfile import ZipFile
from io import BytesIO
import os


class IdebDownload:
    
    root_url = 'https://download.inep.gov.br/educacao_basica/portal_ideb/planilhas_para_download/2019/'
    link_iniciais = root_url + 'divulgacao_anos_iniciais_escolas_2019.zip'
    link_finais = root_url + 'divulgacao_anos_finais_escolas_2019.zip'
    
    path_dados = 'raw_data/ideb_raw'
    
    file_inicias = 'divulgacao_anos_iniciais_escolas_2019/divulgacao_anos_iniciais_escolas_2019.xlsx'
    file_finais = 'divulgacao_anos_finais_escolas_2019/divulgacao_anos_finais_escolas_2019.xlsx'
    
    def download(self, link):
        """Baixa o conteúdo requisitado"""
        
        with requests.get(link) as r:
            content = r.content
        
        return content
    
    def check_dir(self):
        """Checa se o caminho existe"""
        
        if not os.path.exists('raw_data'):
            os.mkdir(self.path_dados)
    
    def unzip(self, content, filename, path_dados):
        """Deszipa o arquivo e retorna o caminho para o arquivo extraido"""
        
        with ZipFile(BytesIO(content)) as ziped:
            if filename not in ziped.namelist():
                raise ValueError(f'{filename} não está no zip. Files:\n {ziped.namelist()}')
            file_path = ziped.extract(filename, path=path_dados)
        
        return file_path
            
    def download_and_unzip_inicias(self):
        """Faz o download e extrai o conteúdo de idebs iniciais"""
        
        print('Baixando dados Ideb: anos iniciais')

        content = self.download(self.link_iniciais)
        
        return self.unzip(content, self.file_inicias, self.path_dados)
    
    def download_and_unzip_finais(self):
        """Faz o download e extrai o conteúdo de idebs finais"""

        print('Baixando dados Ideb: anos finais')
        
        content = self.download(self.link_finais)
        
        return self.unzip(content, self.file_finais, self.path_dados)
    
    def __call__(self, tipo='all'):
        """Chama a si mesmo e faz a download e extração dos idebs inicias e finais"""

        if tipo == 'all':
        
            self.download_and_unzip_inicias()
            print('Anos iniciais Ideb baixados com sucesso')
            self.download_and_unzip_finais()
            print('Anos finais Ideb baixados com sucesso')
        
        elif tipo == 'iniciais':
            self.download_and_unzip_inicias()
            print('Anos iniciais Ideb baixados com sucesso')
        elif tipo == 'finais':
            self.download_and_unzip_finais()
            print('Anos finais Ideb baixados com sucesso')
        else:
            raise ValueError(f'Tipo {tipo} inexistente!')
