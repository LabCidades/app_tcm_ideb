import requests
from bs4 import BeautifulSoup


class DadosAbertos:
    '''
    Callable que retorna um generator contendo o conteudo dos recursos 
    disponíveis para um determinado conjunto no Portal de Dados Abertos da PMSP.
    
    url_cojunto: str, url de acesso do conjunto de dados no Portal de Dados Abertos
    extensoes: extensoes dos conjuntos que se deseja baixar
    '''

    extensoes_suportadas = ('csv', 'xlsx', 'xls', 'txt')
    
    def __init__(self, url_conjunto, extensoes=('csv',)):
        
        self.url_conjunto = url_conjunto
        self.extensoes=extensoes
        self.recursos = self.parse_all_recursos(url_conjunto, extensoes)
    
    def get_page_conjunto(self, url):
        
        with requests.get(url) as r:
            html = r.text
        
        return html
    
    def gerar_sopa(self, html):
        
        return BeautifulSoup(html)
    
    def listar_recursos(self, sopa):
        
        return sopa.find_all('li', {'class' : "resource-item"})
    
    def pegar_extensao(self, link):
        
        return link.split('.')[-1]
    
    def parsear_recurso(self, recurso):
        
        desc = recurso.find('p', {'class' : 'description'}).text.strip()
        link = recurso.find('a', {'class' : "resource-url-analytics"})['href']
        extensao = self.pegar_extensao(link)
        
        dados = {
            'descricao' : desc,
            'extensao' : extensao,
            'link' : link
        } 
        
        return dados
    
    def check_extensao_suportada(self, extensoes_solicitadas):
        
        for extensao in extensoes_solicitadas:
            if extensao not in self.extensoes_suportadas:
                raise NotImplementedError(f'Extensao {extensao} não suportada')
    
    def parse_all_recursos(self, url_conjunto, extensoes=('csv', )):
        
        self.check_extensao_suportada(extensoes)
        
        page_conjunto = self.get_page_conjunto(url_conjunto)
        sopa = self.gerar_sopa(page_conjunto)
        
        parsed_data = []
        recursos_raw = self.listar_recursos(sopa)
        
        for rec in recursos_raw:
            
            parsed_resource = self.parsear_recurso(rec)
            
            if parsed_resource['extensao'] in extensoes:
            
                parsed_data.append(parsed_resource)
            
            else:
                print('Resource não listado por estar fora da extensão solicitada:')
                print(f"{parsed_resource['descricao']} : {parsed_resource['extensao']}")
        
        return parsed_data

                
    def check_if_text_download(self, recurso_parsed):
        
        extensao = recurso_parsed['extensao']
        self.check_extensao_suportada((extensao,))
        
        extensoes_textuais = ('csv', 'txt', 'xls', 'xlsx')
        
        if extensao in extensoes_textuais:
            return True
        return False
    
    def get_content(self, recurso_parsed):
        
        text_download = self.check_if_text_download(recurso_parsed)
        
        if text_download:
            with requests.get(recurso_parsed['link']) as r:
                return r.text
        else:
            with requests.get(recurso_parsed['link']) as r:
                    return r.content
    
    def download_all(self, resource_list):
        
        for resource in resource_list:
            yield self.get_content(resource)
            
    def __call__(self):
        
        return self.download_all(self.recursos)