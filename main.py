import flet as ft

# import pandas as pd

# import webbrowser
# import PySimpleGUI as sg
# import importardadosmembros as ipd
import json
# from gspread_leo import *

import pandas as pd
from operator import attrgetter
import threading
# from concurrent.futures import ThreadPoolExecutor

import time
import random
import os
# from IPython.display import clear_output
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("expand_frame_repr", False)

from vilas_gpt import LayoutVilas,Vila
from jogadores import layout_jogadores,Jogador
from equipes import layout_equipes
from importar import layout_Importar
class My_Dropdown(ft.Dropdown):
    def __init__(self, nome,on_change, *itens):
        super().__init__()
        self.label = nome
        self.options = [ft.dropdown.Option(i) for i in list(itens)]
        self.on_change = on_change
        self.width = 150
        self.value = None
    
class My_tabela(ft.DataTable):
    def __init__(self, df#DataFrame ou dicionário
                 ):
        super().__init__()
        self._df = df if type(df) != dict else pd.DataFrame(df)
        self.border = ft.border.all(1,'white,0.9')
        self.heading_row_color = 'white,0.5'
        self.heading_row_height = 35
        self.column_spacing = 15
        # self.heading_row_color=colors.BLACK12
        self.vertical_lines = ft.border.all(20,'white')
        self.horizontal_margin = 0
        self.data_row_max_height = 35
        # self.data_row_min_height = 50
        self.divider_thickness = 0
        self.show_checkbox_column = True
        self.sort_column_index = 4
        self.sort_ascending = True
        # self.data_row_color={"hovered": "0x30FF0000"}
        self.visible = False
        self.textsize = 15
        self.Colunas_tabela()
        self.Linhas_tabela()

    def Colunas_tabela(self):
        self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM)],alignment='center')) for i in list(self._df.columns)]
        
    
    def Linhas_tabela(self):
        linhas = []
        df_lista = self._df.values.tolist()
        opcoes = [ft.dropdown.Option(i[0]) for i in df_lista]
        for l,i in enumerate(df_lista):
            cell = [ft.DataCell(ft.Row([ft.Dropdown(value = i[0],options=opcoes, dense = True, width=165, content_padding=7)], width=170,
                        alignment='center',spacing = 3,vertical_alignment='center'))]
            cell += [ ft.DataCell(ft.Row([ft.Text(j,text_align='center',selectable = True, size = self.textsize)],
                        alignment='center',spacing = 3,vertical_alignment='center')) for j in i[1:]]
            
            cor  = 'black' if l % 2 == 0 else 'white,0.01'
            linhas.append(ft.DataRow(cells = cell, color = cor))
        self.rows = linhas

    @property
    def df(self):
        return self._df
    @df.setter
    def df(self, df):
        self._df = df if type(df) != dict else pd.DataFrame(df)
        self.Colunas_tabela()
        self.Linhas_tabela()


class My_tabelaE(ft.DataTable):
    def __init__(self, df,#DataFrame ou dicionário
                 on_tap_down = None
                 ):
        super().__init__()
        self._df = df if type(df) != dict else pd.DataFrame(df)
        self.border = ft.border.all(1,'white,0.9')
        self.heading_row_color = 'white,0.5'
        self.heading_row_height = 35
        self.column_spacing = 15
        # self.heading_row_color=colors.BLACK12
        self.vertical_lines = ft.border.all(20,'white')
        self.horizontal_margin = 0
        self.data_row_max_height = 35
        # self.data_row_min_height = 50
        self.divider_thickness = 0
        self.show_checkbox_column = True
        self.sort_column_index = 4
        self.sort_ascending = True
        self.on_tap_down = on_tap_down
        self.tabela = None
        # self.data_row_color={"hovered": "0x30FF0000"}
                
        self.textsize = 15
        self.Colunas_tabela()
        self.Linhas_tabela()

    def Colunas_tabela(self):
        self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM,width=50 if k != 0 else 150)],alignment='center')) for k,i in enumerate(list(self._df.columns))]
        
    
    def Linhas_tabela(self):
        linhas = []
        df_lista = self._df.values.tolist()
        for l,i in enumerate(df_lista):
            cell = [ ft.DataCell(ft.Row([ft.TextField(value = j,text_align='center', content_padding = 0,text_size = self.textsize, dense = True,height= 30, width=50 if k != 0 else 150)],
                    alignment='center',spacing = 3,vertical_alignment='center'), data = [l, k, 'cel'], on_tap_down = None) for k,j in enumerate(i)]
            cor  = 'black' if l % 2 == 0 else 'white,0.01'
            linhas.append(ft.DataRow(cells = cell, color = cor))
        self.rows = linhas

    @property
    def df(self):
        return self._df
    @df.setter
    def df(self, df):
        self._df = df if type(df) != dict else pd.DataFrame(df)
        self.Colunas_tabela()
        self.Linhas_tabela()


    def func(self,e):
        # e.control.data
        valor = e.control.content.controls[0].value
        # self.on_tap_down(valor)
        self.update()

    def Gerar_df(self):
        colunas = self._df.columns
        linhas = [i.cells for i in self.rows]
        linhas2 = []

        for i in linhas:
            l = []
            for j in i:
                l.append(j.content.controls[0].value)
            linhas2.append(l)


        self.tabela =  pd.DataFrame(linhas2,columns=colunas)
        return self.tabela
        




# class Vila:
#     def __init__(self, nome, nivel_cv, forca, cv_exposto, equipe, metodo=2, mapa=None):
#         self.nome = nome
#         self.nivel_cv = nivel_cv
#         self.forca = forca
#         self.cv_exposto = cv_exposto
#         self.estrelas_l = 0
#         self.atacante = 0
#         self.estrela = 0
#         self.metodo = metodo
#         self.mapa = mapa
#         self.equipe = equipe
#         # self.equipes_iniciadas = self.Iniciar_equipe()
#         ''' Equipes'''
#         self.GRUPO_ELITE = int(self.equipe['GRUPO ELITE'])
#         self.GRUPO_A = int(self.equipe['GRUPO A'])
#         self.GRUPO_B = int(self.equipe['GRUPO B'])
#         self.GRUPO_C = int(self.equipe['GRUPO C'])
#         self.GRUPO_D = int(self.equipe['GRUPO D'])
#         self.GRUPO_E = int(self.equipe['GRUPO E'])

#     def recebe_ataque(self, lista_jogadores):

#         if self.metodo == 1:
#             estrelas = 0
#             for jogador in lista_jogadores:
#                 # print('nível do cv do jogador', jogador.nivel_cv)
#                 # print('nível do cv da vila', self.nivel_cv)
#                 # diferença_de_cv = jogador.nivel_cv - self.nivel_cv
#                 # if mostrar_ataques ==1:
#                 #   print(f'{jogador.nome} - cv{jogador.nivel_cv} atacando:')
#                 estrela_temp = 0
#                 if self.cv_exposto == 1:
#                     estrela_temp = 1
#                 # cv do jogador =15

#                 if jogador.nivel_cv == 15:
#                     if self.nivel_cv == 13:
#                         if jogador.forca > 90:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     if self.nivel_cv <= 12:
#                         estrelas = 3
#                     elif self.nivel_cv == 15:
#                         if self.forca < 40:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv == 14:
#                         if self.forca > 60:
#                             estrelas = 2
#                         else:
#                             estrelas = 3

#                 # cv do jogador =14   #################################################
#                 elif jogador.nivel_cv == 14:
#                     if self.nivel_cv <= 12:
#                         if jogador.forca > 50:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv > 14:
#                         if self.forca < 20:
#                             estrelas = 3
#                         else:
#                             if jogador.forca > 50:
#                                 estrelas = 2
#                             else:
#                                 estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 14:
#                         if self.forca < 40:
#                             estrelas = 3
#                         else:
#                             if jogador.forca > 50:
#                                 estrelas = 2
#                             else:
#                                 estrelas = estrela_temp + 1

#                     elif self.nivel_cv == 13:
#                         if jogador.forca > 90:
#                             estrelas = 3
#                         else:
#                             if self.forca < 50:
#                                 estrelas = 3
#                             else:
#                                 estrelas = 2

#                 # cv do jogador =13    #################################################
#                 elif jogador.nivel_cv == 13:
#                     if self.nivel_cv > 14:
#                         if self.forca < 20:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 14:
#                         if self.forca < 20:
#                             estrelas = 3
#                         else:
#                             estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 13:
#                         if self.forca < 30:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv == 12:
#                         if self.forca < 30:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv <= 11:
#                         estrelas = 3
#                 # cv do jogador =12   #################################################
#                 elif jogador.nivel_cv == 12:
#                     if self.nivel_cv > 14:
#                         if self.forca < 20:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 14:
#                         if self.forca < 60:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 13:
#                         if self.forca < 50:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 12:
#                         if self.forca < 20:
#                             estrelas = 3
#                         else:
#                             if jogador.forca > 60:
#                                 estrelas = 2
#                             else:
#                                 estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 11:
#                         if self.forca < 30:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv <= 10:
#                         estrelas = 3

#                 # cv do jogador =11   #################################################
#                 elif jogador.nivel_cv == 11:
#                     if self.nivel_cv > 14:
#                         if self.forca < 20:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 14:
#                         if self.forca < 40:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 13:
#                         if self.forca < 40:
#                             estrelas = 2
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 12:
#                         if self.forca < 20:
#                             estrelas = 3
#                         else:
#                             estrelas = estrela_temp + 1
#                     elif self.nivel_cv == 11:
#                         if self.forca < 40:
#                             estrelas = 3
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv <= 10:
#                         estrelas = 3
#                 # cv do jogador =10   #################################################
#                 elif jogador.nivel_cv == 10:
#                     if self.nivel_cv <= 9:
#                         estrelas = 3
#                     elif self.nivel_cv >= 14:
#                         if self.forca < 20:
#                             estrelas = estrela_temp + 1
#                         else:
#                             estrelas = 1
#                     elif self.nivel_cv == 13:
#                         if self.forca > 20:
#                             estrelas = 2
#                         else:
#                             estrelas = 3
#                     elif self.nivel_cv == 12:
#                         if self.forca > 20:
#                             estrelas = 2
#                         else:
#                             estrelas = 3
#                     elif self.nivel_cv == 11:
#                         if self.forca > 20:
#                             estrelas = 2
#                         else:
#                             estrelas = 3
#                     elif self.nivel_cv == 10:
#                         if self.forca > 80:
#                             estrelas = 2
#                         else:
#                             estrelas = 3

#                 # cv do jogador =9   #################################################
#                 elif jogador.nivel_cv == 9:
#                     if self.nivel_cv <= 8:
#                         estrelas = 3
#                     elif self.nivel_cv == 12:
#                         if self.forca < 20:
#                             estrelas = estrela_temp + 1
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 10:
#                         if self.forca > 50:
#                             estrelas = 2
#                         else:
#                             estrelas = 3
#                     elif self.nivel_cv == 9:
#                         if jogador.forca < 90:
#                             estrelas = 2
#                         else:
#                             estrelas = 3

#                 elif jogador.nivel_cv == 8:
#                     if self.nivel_cv <= 8:
#                         estrelas = 3
#                     elif self.nivel_cv >= 11:
#                         if self.forca < 20:
#                             estrelas = estrela_temp + 1
#                         else:
#                             estrelas = estrela_temp
#                     elif self.nivel_cv == 10:
#                         if self.forca > 50:
#                             estrelas = estrela_temp + 1
#                         else:
#                             estrelas = 2
#                     elif self.nivel_cv == 9:
#                         estrelas = 2

#                 # if mostrar_ataques ==1:
#                 #   print(f'Vila {self.nome} (cv {self.nivel_cv}) faz {estrelas} estrelas')
#                 self.estrelas_l = estrelas

#         if self.metodo in [2, 4]:
#             estrelas = 0
#             for jogador in lista_jogadores:
#                 # print('nível do cv do jogador', jogador.nivel_cv)
#                 # print('força do jogador', jogador.forca)
#                 # print('nível do cv da vila', self.nivel_cv)
#                 # diferença_de_cv = jogador.nivel_cv - self.nivel_cv
#                 # if mostrar_ataques ==1:
#                 #   print(f'{jogador.nome} - cv{jogador.nivel_cv} atacando:')
#                 estrela_temp = 0
#                 if self.cv_exposto == 1:
#                     estrela_temp = 1
#                 # cv do jogador =15

#                 # GRUPO_ELITE = 989
#                 # GRUPO_A = 910
#                 # GRUPO_B = 840
#                 # GRUPO_C = 675
#                 # GRUPO_D = 579
#                 # GRUPO_E = 510

#                 if jogador.forca >= self.GRUPO_ELITE:
#                     if self.nivel_cv <= 14:
#                         estrelas = 3
#                     if self.nivel_cv > 14:
#                         estrelas = 2

#                 if jogador.forca >= self.GRUPO_A and jogador.forca < self.GRUPO_ELITE:
#                     if self.nivel_cv <= 13:
#                         estrelas = 3
#                     if self.nivel_cv > 13:
#                         estrelas = 2

#                 elif jogador.forca >= self.GRUPO_B and jogador.forca < self.GRUPO_A:
#                     if self.nivel_cv <= 12:
#                         estrelas = 3
#                     if self.nivel_cv > 12:
#                         estrelas = 2

#                 elif jogador.forca >= self.GRUPO_C and jogador.forca < self.GRUPO_B:
#                     if self.nivel_cv <= 11:
#                         estrelas = 3
#                     if self.nivel_cv in [12, 13]:
#                         estrelas = 2
#                     if self.nivel_cv >= 14:
#                         estrelas = estrela_temp + 1

#                 elif jogador.forca >= self.GRUPO_D and jogador.forca < self.GRUPO_C:
#                     if self.nivel_cv <= 10:
#                         estrelas = 3
#                     if self.nivel_cv == 11:
#                         estrelas = 2
#                     if self.nivel_cv == 12:
#                         estrelas = 2
#                     if self.nivel_cv == 13:
#                         estrelas = 1 + estrela_temp
#                     if self.nivel_cv >= 14:
#                         estrelas = estrela_temp

#                 elif jogador.forca >= self.GRUPO_E and jogador.forca < self.GRUPO_D:
#                     if self.nivel_cv <= 9:
#                         estrelas = 3
#                     if self.nivel_cv == 10:
#                         estrelas = 2
#                     if self.nivel_cv == 11:
#                         estrelas = estrela_temp + 1
#                     if self.nivel_cv == 12:
#                         estrelas = 1
#                     if self.nivel_cv >= 13:
#                         estrelas = estrela_temp

#                 # if mostrar_ataques ==1:
#                 #   print(f'Vila {self.nome} (cv {self.nivel_cv}) faz {estrelas} estrelas')
#                 # print(f'{jogador.forca} fez {self.estrelas_l} na vila {self.nome}')
#             self.estrelas_l = estrelas

#         if self.metodo == 3:
#             estrelas = 0
#             for jogador in lista_jogadores:
#                 plan = self.mapa
#                 # print(plan)
#                 try:
#                     estrelas = plan.loc[str(jogador.nome), str(self.nome)]
#                 except:
#                     estrelas = plan.loc[str(jogador.nome), str(self.nome)+'.0']
#             self.estrelas_l = estrelas


# class Jogador:
#     def __init__(self, nome, nivel_cv, forca):
#         self.nome = nome
#         self.nivel_cv = nivel_cv
#         self.forca = forca
#         self.peso = 0


class Guerra2:
    def __init__(self, metodo, fase=None, arq_configuracoes=None):
        # super().__init__()
        self.arq_configuracoes = arq_configuracoes
        self.metodo = metodo
        self.fase = fase
        # self.lista_jogadores = self.jogadores()[:]  # chama a função jogadores
        self.lista_jogadores = layout_jogadores(printt = print).Gera_Lista_de_jogadores()
        # self.lista_jogadores
        # self.ord_jogs = self.DefinirPesos()
        # chama a função lista_de_vilas
        self.equipe = self.Buscar_equipe()
        # self.lista_vilas
        if self.equipe != None:
            # self.lista_vilas = self.lista_de_vilas_func()[:]
            # v = layout_vilas(printt = print)
            self.lista_vilas = LayoutVilas(printt = print).Gera_Lista_de_Vilas(self.equipe)
        else:
            None
        self.GerarMapaInicial()
        self.seq = [[0], [0]]
        self.pl = 0
        self.estrelas = 0
        self.parar = False
        self.rodou = False
        self.meus_jogadores = None
        # self.tempo_inicial = 0
        # self.tempo_final = None
        # self.delta_t = None
        self.df = None




    def Buscar_equipe(self):
      equipe = self.Ler_json('config_guerra.json')
      self.equipe = equipe['equipe A']
    #   print(self.equipe)
      return self.equipe
#  Método 4

    def Minhas_contas(self):
        a1 = Ler_celulas2(intervalo="A2:C40",
                          key='13JWOtfPbyPQ4BgerTncnbNsSVEoQMFeHW6aRY4_9I5Q',
                          pagina="minhas",
                          credencial='cliente.json'
                          )

        a = pd.DataFrame(a1, columns=['Jogador', 'cv', 'força']).dropna()
        a = a[a['Jogador'].str.len() > 1].values.tolist()
        j = [i[:3] for i in a]
        # cria uma lista vazia de tamanho zero para armazenas as instâncias Jogadores
        self.meus_jogadores = [Jogador(*h) for h in j]

    def Outras_contas(self):
        if self.meus_jogadores == None:
            self.Minhas_contas()
        nome_meus_jogadores = [i.nome for i in self.meus_jogadores]
        nomes_lista_jogadores = [i.nome for i in self.lista_jogadores]
        nomes_outros_jogadores = list(
            set(set(nomes_lista_jogadores) - set(nome_meus_jogadores)))

        self.outros_jogadores = []
        for i in nomes_outros_jogadores:
            for j in self.lista_jogadores:
                if j.nome == i:
                    self.outros_jogadores.append(j)

    def OrdenarListadeClasses(self, lista, atributo, decrecente=False):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)

    def Resultado_metodo_4(self):
        atacantes = []

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=False)

        lista_de_vilas_forca = self.OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=False)

        
        self.GerarMapaInicial()
        vilas = self.mapa

        # print(lista_de_vilas_forca)
        for i in lista_de_vilas_forca:
            estrelas = max(vilas[str(i.nome)])
            while i.atacante == 0:
                for j in self.lista_jogadores:
                    if vilas.loc[j.nome, str(i.nome)] == estrelas and j.nome not in atacantes:
                        i.atacante = j.nome
                        i.estrela = estrelas
                        atacantes.append(j.nome)
                        break
                estrelas += -1
                if estrelas < 0:
                    i.atacante = ''
                    break
        dic = {'Jogador': [], 'Vilas': [], 'Estrelas': [], 'CV':[]}
        lista_de_vilas_forca = self.OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=True)
        for i in lista_de_vilas_forca:
            dic['Jogador'].append(i.atacante)
            dic['Vilas'].append(i.nome)
            dic['Estrelas'].append(i.estrela)
            dic['CV'].append(i.nivel_cv)

        total_es = sum(dic['Estrelas'])
        dic['Estrelas'].append(total_es)
        dic['Jogador'].append('Total')
        dic['Vilas'].append(' ')
        dic['CV'].append(' ')


        df = pd.DataFrame(dic)
        # df = df.sort_values(by='Vilas')
        # df.to_clipboard(index=False)
        # print(df)
        self.df = df

    def Resultado_outras_contas(self):
        self.Minhas_contas()

        # num_vilas = g.mapa.shape[1] - 1
        atacantes = []
        atacadas = []
        estrelas = []

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=True)
        self.GerarMapaInicial()
        vilas = self.mapa

        minhascontas = self.OrdenarListadeClasses(
            self.meus_jogadores, 'forca', decrecente=True)
        nome_minhas_contas = [i.nome for i in minhascontas]

        lista_de_vilas_forca = [int(list(vilas.columns)[-i])
                                for i in range(1, len(list(vilas.columns)))]

        for i in lista_de_vilas_forca:
            for j in range(1, len(vilas['1'])+1):
                try:
                    if vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j] not in atacantes+nome_minhas_contas:
                        self.lista_vilas[i-1].atacante = vilas[vilas[str(
                            i)] == max(vilas[str(i)])]['Jogador'][-j]
                        estrelas.append(max(vilas[str(i)]))
                        atacadas.append(i)
                        atacantes.append(
                            vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j])
                        # print(vilas[vilas[str(i)]==max(vilas[str(i)])]['Jogador'][-j])
                        break
                except:
                    break

        dic = {'Jogador': atacantes, 'Vilas': atacadas, 'Estrelas': estrelas}

        df = pd.DataFrame(dic)
        df = df.sort_values(by='Vilas')
        self.df = df
        # df.to_clipboard(index=False)

    def Resultado_vilas_q_sobraram(self):
        self.Outras_contas()

        # g.Minhas_contas()
        # print(g.mapa)
        # num_vilas = g.mapa.shape[1] - 1
        atacantes = []
        atacadas = []
        estrelas = []
        outrascontas = self.OrdenarListadeClasses(
            self.outros_jogadores, 'forca', decrecente=True)
        nome_outras_contas = [i.nome for i in outrascontas]

        self.lista_jogadores = self.OrdenarListadeClasses(
            self.lista_jogadores, 'forca', decrecente=True)
        self.GerarMapaInicial()
        vilas = self.mapa

        a1 = Ler_celulas2(intervalo="A1:A46",
                          key='13JWOtfPbyPQ4BgerTncnbNsSVEoQMFeHW6aRY4_9I5Q',
                          pagina="sobra",
                          credencial='cliente.json'
                          )
        try:
            d = list(pd.DataFrame(a1)[0])

            lista_vilas_q_sobraram = [int(d[-i]) for i in range(1, len(d)+1)]

            for i in lista_vilas_q_sobraram:
                for j in range(1, len(vilas['1'])+1):
                    try:
                        if vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j] not in atacantes+nome_outras_contas:
                            self.lista_vilas[i-1].atacante = vilas[vilas[str(
                                i)] == max(vilas[str(i)])]['Jogador'][-j]
                            estrelas.append(max(vilas[str(i)]))
                            atacadas.append(i)
                            atacantes.append(
                                vilas[vilas[str(i)] == max(vilas[str(i)])]['Jogador'][-j])
                            # print(vilas[vilas[str(i)]==max(vilas[str(i)])]['Jogador'][-j])
                            break
                    except:
                        break

            dic = {'Jogador': atacantes, 'Vilas': atacadas, 'Estrelas': estrelas}

            df = pd.DataFrame(dic)
            df = df.sort_values(by='Vilas')
            self.df = df
            # df.to_clipboard(index=False)
        except:
            print('ERRO!')
            print(
                'A aba "sobra" da planlha não está devidamente preecnhida com os números das vilas que sobraram')

        # lista_vilas_q_sobraram = [15,23,22,19,18,17,16,9,8,7,6,5,4,3,2,1]
        # lista_vilas_q_sobraram = [str(i) for i in lista_vilas_q_sobraram]

    def TipoArquivo(self):
        try:
            a = (__file__[-2:])
            return 'py'
        except:
            a = os.getcwd()[-2:]
            return 'jupter'

    def LimparTela(self):
        if self.TipoArquivo() != 'py':
            clear_output()
        else:
            os.system('cls')

    def jogadores(self):
        # a = pd.read_excel('vilas-04-03-2023.xlsx', sheet_name='jogadores').values.tolist()  #recebe todos os valores da aba3 da planilha do google sheets
        # .iloc[:15,:4].values.tolist()  #recebe todos os valores da aba3 da planilha do google sheets
        a = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vR5G05936eje6gI30Y6MBQDoBe8cwDjq72Hm1H0av-wASMT-h-8ud2o6cb5ag4YNsu5WDpe1mWEwOYK/pub?gid=164556332&single=true&output=csv')
        a = a[a['Jogador'].str.len() > 1].values.tolist()
        j = [i[:3] for i in a]
        jg = []  # cria uma lista vazia de tamanho zero para armazenas as instâncias Jogadores
        for h in range(len(j)):  # percorre todos os dados da  lista J
            # adiciona cada uma das instãncias jogadore à lista Jg
            jg.append(Jogador(*j[h]))
        return jg  # Retorna uma lista com todas as instâncias jogadores

    def lista_de_vilas_func(self):
        # criando uma lista de vilas########################################################################################################################################
        # all_rows = pd.read_excel('vilas-04-03-2023.xlsx', sheet_name='Página1').values.tolist() #recebe a planilha vilas do google sheets
        # .iloc[:15,:4].astype(int).values.tolist()
        all_rows = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vR5G05936eje6gI30Y6MBQDoBe8cwDjq72Hm1H0av-wASMT-h-8ud2o6cb5ag4YNsu5WDpe1mWEwOYK/pub?gid=0&single=true&output=csv').iloc[:, :4]
        all_rows = all_rows.dropna().values.tolist()
        lista_vilas = []
        for i in all_rows:
            lista_vilas.append(Vila(*i, equipe=self.equipe,
                                    metodo=2, mapa=None))
            # print(lista_vilas[0].metodo)
        return lista_vilas

    def Embaralhar(self, lista):
        s5 = lista[:]
        random.shuffle(s5)
        return s5

    def gera_alvos_e_estrelas_de_lista_de_vilas_embralhada(self):
        estrelas_01 = []
        alvos_0 = []
        lista_de_vilas_embralhada = self.Embaralhar(self.lista_de_vilas)
        for y, e in enumerate(self.lista_jogadores):
            # print(lista_jogadores[y].nome)
            alvos_0.append(lista_de_vilas_embralhada[y].nome)
            lista_de_vilas_embralhada[y].recebe_ataque([e])
            estrelas_01.append(lista_de_vilas_embralhada[y].estrelas_l)
            # print(f'Vila {lista_de_vilas_embralhada[y].nome} recebendo ataque de {e.nome} resultou em {lista_de_vilas_embralhada[y].estrelas_l} estrelas')

        al_est = [alvos_0, estrelas_01]
        return al_est

    def gera_jogadores_e_estrelas_de_lista_de_jogadores_embralhada(self):
        estrelas_01 = []
        jogadores_0 = []
        lista_de_jogadores_embralhada = self.Embaralhar(self.lista_jogadores)
        for y, e in enumerate(self.lista_vilas):
            # print(lista_jogadores[y].nome)
            jogadores_0.append(lista_de_jogadores_embralhada[y])
            e.recebe_ataque([lista_de_jogadores_embralhada[y]])
            estrelas_01.append(e.estrelas_l)
        al_est = [jogadores_0, estrelas_01]
        return al_est

    def GerarMapaDeEstrelas(self):
        mapa = []
        for i in self.lista_jogadores:
            estrelas_02 = []
            for j in self.lista_vilas:
                # print(i.nome)
                j.recebe_ataque([i])
                estrelas_02.append(j.estrelas_l)
            # i.estrelas = estrelas_02
            mapa.append([i.nome] + estrelas_02)

        gm = pd.DataFrame(
            mapa, columns=['Jogador']+[str(i.nome) for i in self.lista_vilas])
        # gm.to_clipboard()
        # print(gm)
        self.df = gm
        return gm

    def GerarMapa_de_lista(self, lista):
        mapa = []
        for i in lista:
            estrelas_02 = []
            for j in self.lista_vilas:
                # print(i.nome)
                j.recebe_ataque([i])
                estrelas_02.append(j.estrelas_l)
            mapa.append([i.nome] + estrelas_02)

        gm = pd.DataFrame(
            mapa, columns=['Jogador']+[str(i.nome) for i in self.lista_vilas])
        # gm.to_clipboard()
        # self.mada_de_lista = gm
        return gm

    def GerarMapaInicial(self):
        if self.metodo in [3, 4] and self.lista_vilas != None:
            plan = self.GerarMapaDeEstrelas()
            plan.index = plan['Jogador']
            self.mapa = plan
            # print( self.mapa)
            for j in self.lista_vilas:
                j.mapa = self.mapa
                j.metodo = self.metodo
            print('mapa gerado!')
        else:
            self.mapa = None

            # print( self.mapa)

    def Rodar(self,
              ciclos=5000000,
              # lista com poucos ataques de 0 estrela:
              pocucas_0_estrelas=False,
              # lista com poucos ataques de 1 estrela:
              poucas_1_estrelas=False,
              # lista com poucos ataques de 2 estrela:
              poucas_2_estrelas=False,
              poucas_3_estrelas=True,  # lista com poucos ataques de 3 estrela:
              inverter=False,
              ):
        self.rodou = True

        def SinalOp(qtd, sinal='maior'):
            if inverter == False:
                if sinal == 'maior':
                    return self.seq[1].count(qtd) > r1[1].count(qtd)
                elif sinal == 'menor':
                    return self.seq[1].count(qtd) < r1[1].count(qtd)
                elif sinal == 'igual':
                    return self.seq[1].count(qtd) == r1[1].count(qtd)
            else:
                if sinal == 'maior':
                    return self.seq[1].count(qtd) < r1[1].count(qtd)
                elif sinal == 'menor':
                    return self.seq[1].count(qtd) > r1[1].count(qtd)
                elif sinal == 'igual':
                    return self.seq[1].count(qtd) == r1[1].count(qtd)

        def ResultTemp():
            print(f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - {self.seq[1].count(3)} (3 stars) - {self.seq[1].count(2)} (2 stars) - {self.seq[1].count(1)} (1 stars) - {self.seq[1].count(0)} (0 stars)')

        ordenacao = 0
        self.parar = False
        ti = time.time()
        tempo = 15
        duracao = 0
# ['Geral', 'Outras contas', 'Minhas contas']
        if self.metodo == 4:
            if self.fase == 'Geral':
                self.Resultado_metodo_4()
                # self.GerarMapaInicial()
            elif self.fase == 'Outras contas':
                self.Resultado_outras_contas()
            elif self.fase == 'Minhas contas':
                self.Resultado_vilas_q_sobraram()

        elif self.metodo in [1, 2, 3]:
            
            for w in range(ciclos):
                if self.parar:
                    print('Parada')
                    break
                r1 = self.gera_jogadores_e_estrelas_de_lista_de_jogadores_embralhada()
                sr = sum(r1[1])
                ss = sum(self.seq[1])
                if sr > ss:
                    self.seq = r1[:]
                    print(
                        f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - soma maior')
                    self.pl += 1

                elif sr == ss:
                    if poucas_3_estrelas:  # para o caso de querer uma lista final com menos ataques de 3 estrela
                        if SinalOp(3, sinal='maior'):
                            self.seq = r1[:]
                            print(' 3')

                            ResultTemp()
                            self.pl += 1

                        elif SinalOp(3, sinal='igual') and SinalOp(0, sinal='maior'):
                            self.seq = r1[:]
                            print('3 e 0')

                            ResultTemp()
                            self.pl += 1

                    if poucas_2_estrelas:  # para o caso de querer uma lista final com menos ataques de 0 estrela
                        if SinalOp(2, sinal='maior'):
                            self.seq = r1[:]
                            print('2')

                            ResultTemp()
                            self.pl += 1

                    if poucas_1_estrelas:  # para o caso de querer uma lista final com menos ataques de 1 estrela
                        if SinalOp(1, sinal='maior'):
                            self.seq = r1[:]
                            print('1')

                            ResultTemp()
                            self.pl += 1

                    if pocucas_0_estrelas:  # para o caso de querer uma lista final com menos ataques de 0 estrela
                        if SinalOp(0, sinal='maior'):
                            self.seq = r1[:]
                            print(' 0')

                            ResultTemp()
                            self.pl += 1
                        elif SinalOp(0, sinal='igual') and SinalOp(2, sinal='maior'):
                            self.seq = r1[:]
                            print(' 0 e 2')
                            ResultTemp()
                            self.pl += 1


                if self.pl >= 10:
                    # self.LimparTela()
                    self.pl = 0

                tf = time.time()
                delta_t = round(tf-ti, 1)
                if delta_t >= tempo:
                    duracao += tempo
                    duracao = round(duracao, 1)
                    print(
                        f'Estrelas:{self.seq[1]} - Total:{sum(self.seq[1])} - ciclo {w} - time = {duracao}s')
                    ti = time.time()
                    tf = time.time()

    def Resultado(self):
        self.estrelas = self.seq[1]

        self.DefinirAtacantesEEstrelas()

        def OrdenarListadeClasses(lista, atributo, decrecente=False):
            return sorted(lista, key=attrgetter(atributo), reverse=decrecente)

        vilas_ordenadas = OrdenarListadeClasses(
            self.lista_vilas, 'forca', decrecente=True)

        listaj = self.lista_jogadores[:]
        for j, vila in enumerate(vilas_ordenadas):
            if vila.estrela == 3:
                listaj = OrdenarListadeClasses(
                    listaj, 'forca', decrecente=True)
                # print(listaj)
                for n, k in enumerate(listaj):
                    jogador = k
                    vila.recebe_ataque([jogador])
                    if vila.estrelas_l == vila.estrela:
                        vila.atacante = jogador.nome
                        del listaj[n]
                        break
                    # print(f'vila{vila.nome} << {vila.atacante}')

            else:
                listaj = OrdenarListadeClasses(listaj, 'forca', )
                for n, k in enumerate(listaj):
                    jogador = k
                    # print(k.nome)
                    vila.recebe_ataque([jogador])
                    if vila.estrelas_l == vila.estrela:
                        vila.atacante = jogador.nome
                        del listaj[n]
                        break
                    # print(f'vila{vila.nome} << {vila.atacante}')

        result = []
        for j, i in enumerate(self.lista_vilas):
            i.nome = int(i.nome)
            result.append([i.atacante, i.nome, i.estrela])
        newplan = pd.DataFrame(result, columns=['Jogador', 'Alvos', 'Estrelas']).sort_values(
            by=['Alvos'], ascending=True)
        total_de_estrelas = sum(self.estrelas)
        tt = pd.DataFrame({'Jogador': ['Total'], 'Alvos': [
            '  '], 'Estrelas': total_de_estrelas})
        fra = [newplan, tt]
        resu = pd.concat(fra).reset_index(drop=True)
        # resu.to_clipboard()
        self.df = resu
        return resu

    def Resultado2(self):
        if self.rodou:
            self.estrelas = self.seq[1]
            self.DefinirAtacantesEEstrelas()

            def ExibirAtributo(lista, atributo):
                for i in lista:
                    print(i.atributo)

            def OrdenarListadeClasses(lista, atributo, decrecente=False):
                return sorted(lista, key=attrgetter(atributo), reverse=decrecente)

            vilas_ordenadas = OrdenarListadeClasses(
                self.lista_vilas, 'forca', decrecente=True)

            listaj = self.lista_jogadores[:]
            listaj = OrdenarListadeClasses(listaj, 'forca', decrecente=True)

            # for i in vilas_ordenadas:
            #     i.atacante = ''
            def OrdenaJogadoresEstrelas(qtd_estrelas, listaj):
                Nnum_vila_velha = None  # nome da vila que estava sendo atacada pelo jogador anterior
                atacantes_3 = []
                for j, vila in enumerate(vilas_ordenadas):
                    if vila.estrela == qtd_estrelas:
                        # print(listaj)
                        atacante_anterior = vila.atacante
                        # encontra o antacante anterior
                        for i in listaj:
                            if atacante_anterior == i.nome:
                                atacante_anterior = i
                                break

                        for n, k in enumerate(listaj):
                            novo_atacante = k
                            vila.recebe_ataque([novo_atacante])
                            if vila.estrelas_l == vila.estrela:
                                # encontra a vila que estava sendo atacada pelo jogador anterior
                                for m, i in enumerate(vilas_ordenadas):
                                    if i.atacante == novo_atacante.nome:
                                        Nnum_vila_velha = m
                                        break

                                # testa se o anatacante anterior consegue a mesma quantidade de estrlas que o novo jogador conseguia naquela vila
                                vilas_ordenadas[m].recebe_ataque(
                                    [atacante_anterior])
                                if vilas_ordenadas[m].estrelas_l == vilas_ordenadas[m].estrela:
                                    vilas_ordenadas[m].atacante = atacante_anterior.nome
                                    vila.atacante = novo_atacante.nome
                                    atacantes_3.append(novo_atacante)
                                    del listaj[n]
                                    break

                return atacantes_3

            def ReordenaJogadores(qtd_estrelas, atacantes_3):
                for j, vila in enumerate(vilas_ordenadas):
                    if vila.estrela == qtd_estrelas:
                        # print(listaj)
                        atacante_anterior = vila.atacante
                        # print(vila.nome, atacante_anterior)
                        # encontra o antacante anterior
                        for i in atacantes_3:
                            if atacante_anterior == i.nome:
                                atacante_anterior = i
                                # print(atacante_anterior.nome)
                                break

                        for n, k in enumerate(atacantes_3):
                            novo_atacante = k
                            vila.recebe_ataque([novo_atacante])
                            if vila.estrelas_l == vila.estrela:
                                # encontra a vila que estava sendo atacada pelo jogador anterior
                                for m, i in enumerate(vilas_ordenadas):
                                    if i.atacante == novo_atacante.nome:
                                        Nnum_vila_velha = m
                                        break

                                # testa se o anatacante anterior consegue a mesma quantidade de estrlas que o novo jogador conseguia naquela vila
                                vilas_ordenadas[m].recebe_ataque(
                                    [atacante_anterior])
                                if vilas_ordenadas[m].estrelas_l == vilas_ordenadas[m].estrela:
                                    vilas_ordenadas[m].atacante = atacante_anterior.nome
                                    vila.atacante = novo_atacante.nome
                                    del atacantes_3[n]
                                    break

            atacantes_3 = OrdenaJogadoresEstrelas(qtd_estrelas=3, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=3, atacantes_3=atacantes_3)

            atacantes_2 = OrdenaJogadoresEstrelas(qtd_estrelas=2, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=2, atacantes_3=atacantes_2)

            atacantes_1 = OrdenaJogadoresEstrelas(qtd_estrelas=1, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=1, atacantes_3=atacantes_1)

            atacantes_0 = OrdenaJogadoresEstrelas(qtd_estrelas=0, listaj=listaj)

            ReordenaJogadores(qtd_estrelas=0, atacantes_3=atacantes_0)

            result = []
            for j, i in enumerate(self.lista_vilas):
                i.nome = int(i.nome)
                result.append([i.atacante, i.nome, i.estrela, i.nivel_cv])
            newplan = pd.DataFrame(result, columns=['Jogador', 'Alvos', 'Estrelas', 'CV']).sort_values(
                by=['Alvos'], ascending=True)
            total_de_estrelas = sum(self.estrelas)
            tt = pd.DataFrame({'Jogador': ['Total'], 'Alvos': [
                '  '], 'Estrelas': total_de_estrelas,'CV':['']})
            fra = [newplan, tt]
            resu = pd.concat(fra).reset_index(drop=True)
            # resu.to_clipboard()
            self.df = resu
        else:
            print('Você ainda não rodou o programa (Rodar)')

    def ResultadoEspelho(self):
        if len(self.lista_jogadores) == len(self.lista_vilas):
            mapa = self.GerarMapaDeEstrelas()
            mapa.index = mapa['Jogador']
            # print(mapa)
            estrelas = []
            alvos = []
            jogadores = []
            cv = []
            for i, j in enumerate(self.lista_vilas):

                jogadores.append(self.lista_jogadores[i].nome)
                cv.append(j.nivel_cv)
                alvos.append(int(j.nome))
                try:
                    estrelas.append(
                        mapa.loc[str(self.lista_jogadores[i].nome), str(j.nome)])
                except:
                    estrelas.append(
                        mapa.loc[str(self.lista_jogadores[i].nome), str(j.nome)+'.0'])

            dic = {'Jogador': jogadores+['Total'],	'Alvos': alvos +
                [' '],	'Estrelas': estrelas+[sum(estrelas)], 'CV':cv+['']}

            df_espelho = pd.DataFrame(dic)
            # df_espelho.to_clipboard()
            # print(df_espelho)
            self.df = df_espelho
        else:
            print(f'O número de jogadores ({len(self.lista_jogadores)}) deve ser igaula ao número de vilas ({len(self.lista_vilas)})')            

    def DefinirAtacantesEEstrelas(self):
        # alvos = [i.nome for i in self.lista_vilas]
        if len(self.seq[0]) >1:
            nomes_dos_jogadores = self.seq[0]
            estrelas = self.seq[1]
            # newplan = pd.DataFrame(
            # {'Jogador': nomes_dos_jogadores, 'Alvos': alvos, 'Estrelas': estrelas}).sort_values(by = ['Alvos'], ascending=True)
            # rl = newplan.values.tolist()
            # for i in rl:
            #     for j in g2.lista_vilas:
            #         if j.nome == i[1]:
            #             j.atacante == i[0]

            for j, i in enumerate(self.lista_vilas):
                i.atacante = nomes_dos_jogadores[j].nome
                # print(nomes_dos_jogadores[j].nome)
                i.estrela = estrelas[j]
        else:
            print('Você ainda não rodou o programa')

    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'w') as f2:
            json.dump(nomedodicionario, f2, indent=4)

    def Ler_json(self, nomedoarquivo):  # retorna um dicionário
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'r') as f2:
            try:
                a = json.load(f2)
                return a
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                return {}


# g2 = Guerra2(metodo=None, equipe=None, fase=None, arq_configuracoes='config_guerra.json')

       
class LayoutGuerra(ft.Row):
    def __init__(self):
        super().__init__()
        self.num_estrelas = False, False, False, True
        self.alignment=ft.MainAxisAlignment.START
        self.g2 = None
        self.api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw 6Z2FtZWFwaSIsImp0aSI6ImYxMjM0OWViLTdjZTMtNGJlZi05N2YwLWVjNjJiZjcwODBiMSIsImlhdCI6MTcwMjY0NTA0Niwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYtNzM2Yy03YzIxL TE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3Ny4z OS41OS4zNyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.21xPvBHTivFI4Artdjns0l780mxVs5KPffY09j_LSEQ46eW1IEZDie1FdhQzHozMFOJLidqL6AsQsgjg_Zc3PA'
        self.link_clan = 'https://api.clashofclans.com/v1/clans/%23299GCJ8U'
        self.link_player = 'https://api.clashofclans.com/v1/players/%23'
        self.fase = 'Geral'
        self.n_ciclos = 50000000


        def Valor(e):
            match e.data:
                case 'poucas_0_estrelas':
                    self.num_estrelas =  True, False, False, False                
                case  'poucas_1_estrelas':
                    self.num_estrelas =  False, True, False, False                  
                case 'poucas_2_estrelas':
                    self.num_estrelas =  False, False, True, False                  
                case  'poucas_3_estrelas':
                    self.num_estrelas =  False, False, False, True   
                               
        def copiar_areaT(e):
            self.g2.df.to_clipboard()
            print('tabela copiada com sucesso!')

        estrelas = My_Dropdown('estrelas',Valor,'poucas_0_estrelas', 'poucas_1_estrelas', 'poucas_2_estrelas', 'poucas_3_estrelas' 
            
        )



        estrelas.value = 'poucas_3_estrelas'
        self.inverter =  ft.Checkbox(label="Inverter", value=False) 
        self.metodo = My_Dropdown('Método',None, 1,2,3,4)
        self.metodo.value = 4
        self.metodo.width = 100
        rodar =ft.ElevatedButton('Rodar', on_click = self.Rodar)
        parar =ft.ElevatedButton('parar', on_click = self.Parar)
        gerar_mapa =ft.ElevatedButton('gerar_mapa',on_click = self.Gerar_mapa)
        resultado2 =ft.ElevatedButton('resultado2',on_click = self.Resultado2)
        resultado_espelho = ft.ElevatedButton('resultado espelho',on_click = self.Resultado_espelho)
        copiar = ft.IconButton(icon = ft.icons.COPY, tooltip = 'copiar tabela para área de transferência', on_click= copiar_areaT)
        self.saida = ft.Text('')
        
        df = pd.DataFrame({'Jogador':list(range(15)), 'Vila':list(range(15)), 'Estrelas': list(range(15))})

        self.tabela = My_tabela(df)
        self.controls = [
            ft.Column([
            ft.Row(height=10),
                ft.Row([estrelas, self.inverter,self.metodo]),
                ft.Row([rodar, resultado2,gerar_mapa,]),
                ft.Row([resultado_espelho,parar,copiar]),
                ft.Container(content = ft.Column([self.saida], auto_scroll=True, scroll=ft.ScrollMode.ADAPTIVE,height = 400, width=350), bgcolor='white,0.01')
            ],alignment=ft.MainAxisAlignment.START, width=350),
            ft.Column([self.tabela])
            
        ]


    def Rodar(self,e):
        pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas = self.num_estrelas
        # print(pocucas_0_estrelas,poucas_1_estrelas,poucas_2_estrelas,poucas_3_estrelas)
        inverter = self.inverter.value
        metodo = int(self.metodo.value)
        # print(metodo)

        print('iniciando ...')
        self.g2 = Guerra2(metodo=metodo,  fase=self.fase,
                    arq_configuracoes='config_guerra.json')
        if self.g2.rodou:
            t1.join()
            self.g2.rodou = False
        t1 = threading.Thread(target=self.g2.Rodar, args=(self.n_ciclos, pocucas_0_estrelas,
                                                    poucas_1_estrelas, poucas_2_estrelas, poucas_3_estrelas, inverter), daemon=True)
        t1.start()
        
        
        if metodo == 4:
            t1.join()
            # time.sleep(10)
            df = self.g2.df
            # print(df)
            self.tabela.visible = True
            self.tabela.df = df# = My_tabela(df)
            # self.tabela.df = self.g2.df
            self.RedimensionarJanela(500)
            self.update()
        # print(self.g2.df)

 
    def Parar(self,e):
        try:
            if self.g2 != None:
                self.g2.parar = True
        except:
            pass

    def resultado(self,e):
        def pp():
            self.g2.Resultado()
            self.tabela.df = self.g2.df
            self.RedimensionarJanela(400)
            self.update()

        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value)
        threading.Thread(target=pp, daemon=True).start()

    def Resultado2(self,e):
        def pp():
            if self.g2.rodou:
                self.g2.Resultado2()
                self.tabela.visible = True
                self.tabela.df = self.g2.df
                self.RedimensionarJanela(425)
                self.update()
            else:
                print('Você ainda não rodou o programa, usando metódo 2')


        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value)
        threading.Thread(target=pp, daemon=True).start()

    def Resultado_espelho(self,e):
        def pp():
            self.g2.ResultadoEspelho()
            self.tabela.visible = True
            self.tabela.df = self.g2.df
            self.RedimensionarJanela(400)
            self.update()

        if self.g2 == None:
            self.g2 = Guerra2(metodo=self.metodo.value)

        threading.Thread(target=pp, daemon=True).start()


    def Gerar_mapa(self,e):
        def pp():
            self.tabela.visible = True
            self.tabela.df = self.g2.GerarMapaDeEstrelas()

            self.update()
        # if self.g2 == None:
        self.g2 = Guerra2(metodo=self.metodo.value)
        threading.Thread(target=pp, daemon=True).start()
        
        self.RedimensionarJanela(650)

    def RedimensionarJanela(self, valor):       
        tamanho = 30*(len(self.g2.lista_jogadores)-4)+valor
        self.page.window_width = tamanho
        self.page.update()

class ConfirmarSaida:
    def __init__(self,page, funcao = None):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.on_window_event = self.window_event
        self.page.window_prevent_close = True 
   


    def window_event(self, e):
            if e.data == "close":
                self.page.dialog = self.confirm_dialog
                
                self.confirm_dialog.open = True
                self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window_destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self,page):
        self.page = page
        self.page.on_resize = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        self.page.overlay.append(self.pw)   

    def page_resize(self, e):
        self.pw.value = f"{self.page.window_width}*{self.page.window_height} px"
        self.pw.update()
  
class Saida(ft.Column):
    def __init__(self):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=150,  ),bgcolor='white,0.03' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.page.update()

class Tabe(ft.Tabs):
    def __init__(self,  funcao = None, *controls):
        super().__init__()
        self.selected_index=0
        self.animation_duration=3
        self.expand=1
        self.controls = list(controls)
        self.funcao = funcao
        self.on_change = self.func
        if isinstance(self.controls, list) and len(self.controls) >0:
            for i in self.controls: 
                if len(i) == 2:                
                    self.tabs.append(ft.Tab(icon=i[0],content=i[1] ))
                else:
                    self.tabs.append(ft.Tab(text=i[0],content=i[1] ))


    def Add(self, icone, janela):
        self.tabs.append(ft.Tab(icon=icone,content=janela ))
        try:
            self.update()
        except:
             pass

    def func(self,e):
        if self.funcao != None:
            self.funcao(e)
        # pass

    

layout = LayoutGuerra()
def print(texto):
    layout.saida.value += f'{texto}\n'
    layout.saida.update()


def main(page: ft.Page):
    page.window_width = 500  # Define a largura da janela como 800 pixels
    page.window_height = 770  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    # saida = Saida() 
    ConfirmarSaida(page)
    Resize(page)    

    vilas = LayoutVilas(printt=print)
    jogadores = layout_jogadores(printt=print)
    equipes = layout_equipes()
    importar = layout_Importar(printt=print)

    def Func(e):
        match e.data:
            case '4':
               page.window_width = 630
               page.window_height = 970
               page.update()             
            case '3':
               page.window_width = 700
               page.update() 
            case '2':
               page.window_width = 500
               page.update()  
            case '1':
               page.window_width = 510
               page.update()  
            case '0':
               page.window_width = 750
               page.update()                                            


    layout2 = Tabe(
        Func,
        ('Lista de Guerra', layout,1),
        ('Vilas',vilas,1),
        ('Jogadores',jogadores,1),
        ('Equipes',equipes,1),
        ('Importar',importar,1)
        
    )
    page.add(layout2)




if __name__ == '__main__':
    # saida = Saida()
    # print = saida.pprint      
    ft.app(main,
    #    view = ft.AppView.WEB_BROWSER
    # port = 8050
       )