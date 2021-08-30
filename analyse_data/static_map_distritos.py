import matplotlib.pyplot as plt
from .regionalizar_distritos import RegionalizarDistritos
from get_data import get_distritos


class StaticMapMakerIdeb:

    def solve_dados_distrito(self, dados_por_distrito=None, tipo_ideb=None):

        if dados_por_distrito is None:
                if tipo_ideb not in ('iniciais', 'finais'):
                    raise ValueError(f'''If dados_por_distrito is None must specify tipo_distrito.
                                    Accepted values are: "finais" or "iniciais"''')
                regionalizar = RegionalizarDistritos()
                dados_por_distrito = regionalizar(tipo_ideb)
        
        return dados_por_distrito

    def get_limites_distritos(self):

        boundary_distritos = get_distritos()['geometry'].boundary

        return boundary_distritos

    def gerar_title(self, tipo_ideb):

        if tipo_ideb is None:
            return f'Ideb Médio por Distrito'

        title = f'Ideb Médio por Distrito - Anos {tipo_ideb.capitalize()}'

        return title


    def gerar_mapa_estatico(self, dados_por_distrito=None, tipo_ideb=None):

        dados_por_distrito = self.solve_dados_distrito(dados_por_distrito, tipo_ideb)
        limites = self.get_limites_distritos()
        titulo_mapa = self.gerar_title(tipo_ideb)

        fig, ax = plt.subplots()
        fig.set_size_inches(8.27, 11.69) #A4 Portrait
        ax =dados_por_distrito.plot(ax=ax, column='ideb_2019', legend=True, 
                    legend_kwds={'label': "Ideb médio",'orientation': "vertical"}, cmap='Reds',
                    alpha=0.5, edgecolor='k')
        ax.set_title(titulo_mapa, size=20)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        limites.plot(ax=ax, color='black', linewidth=0.75)

        ax.get_figure().savefig('mapa_calor_distritos.jpg', transparent=False)

        return ax

    def __call__(self, tipo_ideb):

        return self.gerar_mapa_estatico(tipo_ideb=tipo_ideb)




    
    
