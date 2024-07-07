import json
import pickle
import flet as ft
import re
import webbrowser
import requests
from operator import attrgetter

from pandas import DataFrame

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
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=80,  ),bgcolor='white,0.03' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.page.update()
  
class Players2(ft.DataTable):
    def __init__(self, df = None,#DataFrame ou dicionário
                 func = None
                 ):
        super().__init__()
        self.func = func
        if type(df) == dict:
            self._df = DataFrame(df)
        elif isinstance(df, DataFrame):
            self._df = df 
        else:
            self._df = None 
        
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
        self.visible = True
        self.textsize = 15
        if isinstance(self._df, DataFrame):
            self.Colunas_tabela()
            self.Linhas_tabela()
        else:
            print('não é')


    def Colunas_tabela(self):
        self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM)],alignment='center')) for i in list(self._df.columns)]
        
    
    def Linhas_tabela(self):
        linhas = []
        df_lista = self._df.values.tolist()
        for l,i in enumerate(df_lista):
            # cell = [ ft.DataCell(ft.Row([ft.Text(j,text_align='center',selectable = True, size = self.textsize)],alignment='center',spacing = 3,vertical_alignment='center')) for j in i]

            cell = []
            cell.append(ft.DataCell((ft.Row([ft.Checkbox(value = i[0])],alignment='center',spacing = 3,vertical_alignment='center'))))
            cell += [ ft.DataCell(ft.Row([ft.Text(j,text_align='center',selectable = True, size = self.textsize)],alignment='center',spacing = 3,vertical_alignment='center')) for j in i[1:5]]
            cell.append(ft.DataCell(ft.Row([ft.TextField(value = i[5], width=70,keyboard_type = "number",  bgcolor= 'white,0.08',dense=True, content_padding=5, data = l,on_change=self.chenge_atenuador)],alignment='center',spacing = 3,vertical_alignment='center')))
            cell.append(ft.DataCell(ft.Row([ft.Text(i[6],text_align='center',selectable = True, size = self.textsize)],alignment='center',spacing = 3,vertical_alignment='center')))

            cor  = 'black' if l % 2 == 0 else 'white,0.01'
            linhas.append(ft.DataRow(cells = cell, color = cor))
        self.rows = linhas

    def chenge_atenuador(self,e):
        linha = int(e.control.data)
        valor = e.control.value
        forca = self.rows[linha].cells[4].content.controls[0].value
        try:
            forca_final = int(valor) + int(forca)
            self.rows[linha].cells[6].content.controls[0].value = forca_final
            if self.func != None:
                self.func(e,forca_final)        
        except:
            pass

        self.page.update()


    @property
    def df(self):
        return self._df
    @df.setter
    def df(self, df):
        self._df = df if type(df) != dict else DataFrame(df)
        self.Colunas_tabela()
        self.Linhas_tabela()

class Players(ft.Row):
    def __init__(self, 
                 guerra = None,
                 jogador = None, 
                 tag = None,
                 nivel_cv = None, 
                 forca = None, 
                 atenuador = None,
                 forca_final = None,
                 func = None,
                #  page  = None            
                                  
                 ):
        super().__init__() 
        # self.page = page         
        self.func = func
        self._guerra = ft.Checkbox(value = guerra, data = 'guerra', on_change=self.Chenge_guerra)
        self._jogador = ft.Text(jogador,text_align='center',selectable = True, width=150)
        self._tag = ft.Text(tag,text_align='center',selectable = True, width=100)
        self._nivel_cv = ft.Text(nivel_cv,text_align='center',selectable = True, width=50)
        self._forca = ft.Text(forca,text_align='center',selectable = True, width=80)
        self._atenuador = ft.TextField(value = atenuador,   bgcolor= 'white,0.08',dense=True, 
                            data = 'atenuador',content_padding=5, width=80, on_change=self.Chenge_atenuador)
        
        self._forca_final = ft.Text(forca,text_align='center',selectable = True, width=80)
        self._forca_final.value = forca
        try:
            self._forca_final.value -= int(atenuador)
        except:
            pass

        self.controls = [self._guerra,
                         self._jogador, 
                         self._tag,
                         self._nivel_cv,
                         self._forca,
                         self._atenuador,
                         self._forca_final

        ]


        self.tight = True
        self.spacing = 0
        self.run_spacing = 0

    @property
    def forca_final(self):
        return self._forca_final.value
    

    @property
    def jogador(self):
        return self._jogador.value



    @property
    def guerra(self):
        return self._guerra.value

    @property
    def jogador(self):
        return self._jogador.value

    @property
    def tag(self):
        return self._tag.value

    @property
    def nivel_cv(self):
        return self._nivel_cv.value

    @property
    def forca(self):
        return self._forca.value

    @property
    def atenuador(self):
        return self._atenuador.value   

    def Chenge_guerra(self, e):
        if self.func(e) != None:
            self.func(e)        

    def Chenge_atenuador(self, e):
        valor = self._atenuador.value
        forca = self._forca.value
        try:
            forca_final = int(forca) - int(valor)
            self._forca_final.value = forca_final
            if self.func(e) != None:
                self.func(e)
        except:
            try:
                self._forca_final.value = int(forca)
                if self.func(e) != None:
                    self.func(e)
            except:
                pass            
        # self._forca_final.update()

class layout_Importar(ft.Column):
    def __init__(self, printt = None, page = None):
        super().__init__()
        self.printt = printt
        self.link_clan = 'https://api.clashofclans.com/v1/clans/%23299GCJ8U'
        self.link_player = 'https://api.clashofclans.com/v1/players/%23'        
        self.Tokken = ft.TextField(label='Tokken', width=400,dense=True, content_padding=10, bgcolor='white,0.08',)
        self.Tokken.value ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZkMWVmYTA0LThiM2UtNDVmOS04MjBhLTBmNDU4MzRiYjNhMiIsImlhdCI6MTcyMDAwOTIxMCwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYt NzM2Yy03YzIxLTE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3Ny4zOS41OS4xMDQiXSwidHlwZSI6ImNsaWVudCJ9XX0.YxNIPY1aacWBNIHM7ALWfmh4yYcBztwPeq3gtJx6Fzo2FN5RGk3gZjCo5RlnbYqxhNtNpiT7TCO2FikZK8AdEA'
        # self.tag = ft.TextField(label='tag do clan', width=400,dense=True, content_padding=10, bgcolor='white,0.08',)
        self.tag = ft.Dropdown(label = 'escolha a tag do clan:', 
        options=[ft.dropdown.Option("Aracaju"),ft.dropdown.Option("SkyWarrios"),ft.dropdown.Option("Outro") ], 
        value = "Aracaju",content_padding=10,filled=True, bgcolor='white,0.08'
                )
        # dica = ft.Text('gere o token no site: https://developer.clashofclans.com/#/key/e7ff0da5-5d92-42b7-990f-d7431f5ab41c', color = 'white,0.6',selectable = True)
        self.gerar_token = ft.IconButton(tooltip='gerar Token',icon = ft.icons.GENERATING_TOKENS, on_click=self.GerarToken, icon_size=20)
        self.botao_importar = ft.ElevatedButton('Importar dados',on_click=self.Importar_players)
        
        self.botao_ordenar_guerra = ft.TextButton('Guerra',data = 'guerra',on_click=self.Ordenar_por, width=70)
        self.botao_ordenar_jogador = ft.TextButton('Jogador',data = 'jogador',on_click=self.Ordenar_por, width=80)
        self.botao_ordenar_tag = ft.TextButton('Tag',data = 'tag',on_click=self.Ordenar_por, width=100)
        self.botao_ordenar_cv = ft.TextButton('CV',data = 'nivel_cv',on_click=self.Ordenar_por, width=50)
        self.botao_ordenar_forca = ft.TextButton('Força',data = 'forca',on_click=self.Ordenar_por, width=60)
        self.botao_ordenar_atenuador = ft.TextButton('Atenuador',data = 'atenuador',on_click=self.Ordenar_por, width=95)
        self.botao_ordenar_forca_final = ft.TextButton('Força Final',data = 'forca_final',on_click=self.Ordenar_por, width=60)

        self.controls = [self.tag,self.Tokken,ft.Row([self.botao_importar,self.gerar_token]),
                         
                         ft.Row([
                             self.botao_ordenar_guerra,
                             self.botao_ordenar_jogador,
                             self.botao_ordenar_tag,
                             self.botao_ordenar_cv,
                             self.botao_ordenar_forca,
                             self.botao_ordenar_atenuador,
                             self.botao_ordenar_forca_final,

                                 
                                 
                        ]),
                         
                ]
    
        try:
            self.lista = self.LerPickle('tabela')
            self.tabela = [Players(*i,func = self.Salvar)  for i in self.lista]
            self.tabela = self.OrdenarListadeClasses(self.tabela, 'forca_final')
            self.controls.append(ft.Column(self.tabela,scroll=ft.ScrollMode.ADAPTIVE, height=600))
        except:
            pass
        self.run_spacing = 0
        self.spacing = 0


# i.Tokken.value = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03 ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw 6Z2FtZWFwaSIsImp0aSI6IjI2ODk2ZTg4LTZmYmMtNDU3NS1iYjhkLTI1NWVmM2QzNTMxOSIsI mlhdCI6MTcxNzMzNTIxMiwic3ViIjoiZGV2ZWxvcGVyLzJiNjI4OWNiLTVkOGYtNzM2Yy03YzI xLTE1NmY4NzVjMTVmOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE 3Ny4zOS41OS4xNiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.0uaDqGBq6ayrNLsuaHUTY98uq5AllD5vitRCLlssnl5Ol9rmT_qPleO87kDaGwNF8FEEXNWJ6t7rCElh6A-0EA'
    def OrdenarListadeClasses(self, lista, atributo, decrecente=True):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)    

    def Ordenar_por(self, e):
        atr = e.control.data
        # self.tabela = self.OrdenarListadeClasses(self.tabela, atr)
        self.controls[-1].controls = self.OrdenarListadeClasses(self.controls[-1].controls, atr)
        # self.controls = [self.tag,self.Tokken,ft.Row([self.botao_importar,self.gerar_token]),
                                
        #                         ft.Row([
        #                             self.botao_ordenar_guerra,
        #                             self.botao_ordenar_jogador,
        #                             self.botao_ordenar_tag,
        #                             self.botao_ordenar_cv,
        #                             self.botao_ordenar_forca,
        #                             self.botao_ordenar_atenuador,
        #                             self.botao_ordenar_forca_final,

                                        
                                        
        #                         ]),
        #                         ft.Column(self.tabela,scroll=ft.ScrollMode.ADAPTIVE, height=600)
                                
        #                 ]  
        # for i in self.tabela:
        #     i.update()
        self.update()     
        print(f'ordenando por {atr}')
        self.page.update()

    def Salvar(self,e):
        dic = {'nome':[],'nivel_cv':[],'forca':[] }
        lista = []

        for i in self.tabela:
            if i.guerra:
                dic['nome'].append(i.jogador)
                dic['nivel_cv'].append(i.nivel_cv)
                dic['forca'].append(i.forca_final)

            lista.append([i.guerra,i.jogador,i.tag,i.nivel_cv, i.forca,i.atenuador, i.forca_final])
        
        df = DataFrame(dic)
        df = df.sort_values(by = 'forca', ascending=False)

        df = df.to_dict('list')

        self.SalvarPickle(lista, 'tabela')
        self.Escrever_json(df, 'jogadores_config')
        self.printt('Dados dos players salvo com sucesso') 
        self.update()       



    def GerarToken(self,e):
        webbrowser.open('https://developer.clashofclans.com/#/key/e7ff0da5-5d92-42b7-990f-d7431f5ab41c')

    def _ImportarDadosAPI(self, api_key1, url):
        api_key = re.sub(r'\s+', '', api_key1)
        headers = {'Authorization': f'Bearer {api_key}'}
        # try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # A solicitação foi bem-sucedida, você pode continuar a trabalhar com os dados da API
            # Converte a resposta JSON em um dicionário Python ou uma lista, dependendo do formato dos dados da API
            dados = response.json()
            # Agora, você pode acessar os dados como faria com qualquer outro dicionário ou lista em Python
            return dados
        else:
            # A solicitação não foi bem-sucedida, lide com isso de acordo com os requisitos do seu aplicativo
            return f'Erro ao buscar dados da API. Código de status: {response.status_code}'
    # except:
        #     print('Tokken inválido!')

    def _Import(self, api_key):
        players = self._ImportarDadosAPI(api_key, self.link_clan)
        if isinstance(players, dict):
            tags_nomes = [[i['tag'], i['name']] for i in players['memberList']]

            dic_jogadores = {}
            for i in tags_nomes:
                dic_jogadores[f'{i[1]}-{i[0]}'] = self._ImportarDadosAPI(
                    api_key, url=str(self.link_player+f'{i[0][1:]}'))

            dic_jogadores_esp1 = {}

            chaves_desejadas = ['name', 'townHallLevel',
                                'troops', 'heroes',  'spells']

            dic_jogadores_esp1['nome'] = list(dic_jogadores.keys())

            dic_jogadores_esp1['cv'] = [dic_jogadores[chave]['townHallLevel']
                                        for chave in dic_jogadores_esp1['nome']]

            nomes_herois = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['heroes']]
            
            herois = {chave: dic_jogadores[chave]['heroes']
                    for chave in dic_jogadores_esp1['nome']}
            
            herois2 = {}
            for chave, valor in herois.items():
                herois2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_herois:
                dic_jogadores_esp1[i] = []
                for chave, valor in herois2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            # Valores dos níveis das tropas
            nomes_tropas = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['troops']]
            tropas = {chave: dic_jogadores[chave]['troops']
                    for chave in dic_jogadores_esp1['nome']}
            tropas2 = {}
            for chave, valor in tropas.items():
                tropas2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_tropas:
                dic_jogadores_esp1[i] = []
                for chave, valor in tropas2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            # Valores dos níveis dos spells
            nomes_spells = [i['name']
                            for i in dic_jogadores['lulmor-#2R0GPQC8']['spells']]
            spells = {chave: dic_jogadores[chave]['spells']
                    for chave in dic_jogadores_esp1['nome']}
            spells2 = {}
            for chave, valor in spells.items():
                spells2[chave] = {i['name']: i['level'] for i in valor}

            for i in nomes_spells:
                dic_jogadores_esp1[i] = []
                for chave, valor in spells2.items():
                    # print(i, valor[i])
                    try:
                        dic_jogadores_esp1[i].append(valor[i])
                    except:
                        dic_jogadores_esp1[i].append(0)

            dic_jogadores_esp1['nome'] = [
                i[:-10].replace("-", "") for i in dic_jogadores_esp1['nome']]
            df = DataFrame(dic_jogadores_esp1)
            # df.to_clipboard()
            return df
        else:
            print(f'Tokken inválido!')

    def Importar_dados(self,e):
        api_key = re.sub(r'\s+', '', self.Tokken.value)
        if isinstance(api_key, str) and api_key not in ['', None]:
            print('Importando dados...')
            return self._Import(api_key)
        else:
            self.printt('Você não inseriu uma api_key válida, ou o IP está incorreto. \nVerifique o IP e adicione uma nova api_key no site: \nhttps://developer.clashofclans.com/#/')


    def Testar_tabela(self,e):
        df = DataFrame({'Jogador':list(range(15)),
                         'Vila':list(range(15)), 
                         'Estrelas': list(range(15)),
                         'Estrelas1': list(range(15)),
                         'Estrelas2': list(range(15)),
                         'Estrelas3': list(range(15)),
                         'Estrelas4': list(range(15)),
                         
                         })

        self.tabela.df = df      
        self.update()

    def Importar_players(self,e):
        if self.Tokken.value not in ['', None]:
            self.printt('Importando dados...')
            players1 = self._ImportarDadosAPI(self.Tokken.value, self.link_clan)
            if isinstance(players1, dict):
                self.printt('Nomes dos players importados')

                tags_nomes = [[i['tag'], i['name']] for i in players1['memberList']]

                self.printt('Importando dados de cada um dos players...')

                dic_jogadores = {}
                for j in tags_nomes:
                    dic_jogadores[f'{j[1]}-{j[0]}'] = self._ImportarDadosAPI(self.Tokken.value, url=str(self.link_player+f'{j[0][1:]}'))
                
                def Calcular_forcaT(jogador):
                    cv = jogador['townHallLevel']
                    tropas = jogador['troops']
                    tropas_desejadasT = list((



                        # 'Root Rider', 'L.A.S.S.I', 'Mighty Yak', 'Electro Owl', 'Unicorn',
                        # 'Phoenix', 'Poison Lizard', 'Diggy', 'Frosty', 'Spirit Fox', 'Angry Jelly',

                'Barbarian',
                'Archer',
                'Goblin',
                'Giant',
                'Wall Breaker',
                'Balloon',
                'Wizard',
                'Healer',
                'Dragon',
                'P.E.K.K.A',
                'Minion',
                'Hog Rider',
                'Valkyrie',
                'Golem',
                'Witch',
                'Lava Hound',
                'Bowler',
                'Baby Dragon',
                'Miner',



                'Wall Wrecker',
                'Battle Blimp',
                'Yeti',
                'Sneaky Goblin',
                'Rocket Balloon',
                'Ice Golem',
                'Electro Dragon',
                'Stone Slammer',
                'Inferno Dragon',

                'Dragon Rider',

                'Siege Barracks',
                'Ice Hound',
                'Log Launcher',
                'Flame Flinger',

                'Electro Titan',
                'Apprentice Warden',
                'Super Hog Rider',
                'Root Rider',
                'L.A.S.S.I',
                'Mighty Yak',
                'Electro Owl',
                'Unicorn',
                'Phoenix',
                'Poison Lizard',
                'Diggy',
                'Frosty',
                'Spirit Fox',
                'Angry Jelly'        


                    ))
                
                    forca = []

                    for k in tropas:
                        if k['name'] in tropas_desejadasT:
                            forca.append(5)

                    forca.append(100*cv)
                    return cv, sum(forca)

                def Calcular_forcaH(jogador):
                    heroes = jogador['heroes']
                    tropas_desejadas = list((

                        'Barbarian King', 'Archer Queen', 'Grand Warden', 'Royal Champion',

                    ))

                    forca = []

                    for k in heroes:
                        if k['name'] in tropas_desejadas:
                            forca.append(10)

                    return sum(forca)

                def Calcular_forcaS(jogador):
                    spells = dic_jogadores[j]['spells']

                    tropas_desejadas = list((
                        'Lightning Spell',
                        'Healing Spell',
                        'Rage Spell',
                        'Jump Spell',
                        'Freeze Spell',
                        'Poison Spell',
                        'Earthquake Spell',
                        'Haste Spell',
                        'Clone Spell',
                        'Skeleton Spell',
                        'Bat Spell',
                        'Invisibility Spell',
                        'Recall Spell',
                        'Overgrowth Spell'
                    ))

                    forca = []

                    for k in spells:
                        if k['name'] in tropas_desejadas:
                            forca.append(5)
                    return sum(forca)

                self.lista = []
                for j in list(dic_jogadores.keys()):
                    # j = list(dic_jogadores.keys())[0]
                    nome = dic_jogadores[j]['name']
                    tag = dic_jogadores[j]['tag']
                    cv, forcaT = Calcular_forcaT(dic_jogadores[j])
                    forcaH = Calcular_forcaH(dic_jogadores[j])
                    forcaS = Calcular_forcaS(dic_jogadores[j])
                    forca = forcaT+forcaH+forcaS

                    # dic['Guerra'].append(0)
                    # dic['jogador'].append(nome)
                    # dic['tag'].append(tag)
                    # dic['cv'].append(cv)
                    # dic['forca'].append(forca)
                    # dic['atenuador'].append('')
                    # dic['forca final'].append('')

                    self.lista.append([0,nome,tag,cv,forca, '',''])

                # self.df = DataFrame(dic).sort_values(by = 'forca', ascending=False)

                self.tabela = [Players(*i,self.Salvar)  for i in self.lista]

                # self.SalvarPickle(self.tabela, 'tabela3')

                self.tabela = self.OrdenarListadeClasses(self.tabela, 'forca_final')

                self.Salvar(1)


                self.printt('Dados importados com sucesso!')
                self.update()
                
                
            else:
                self.printt('Erro na importação dos dados')

        else:
            self.printt('Insira o token')



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
            
    def SalvarPickle(self, var, nome):
        with open(nome+'.plk', 'wb') as arquivo:
            pickle.dump(var, arquivo)

    def LerPickle(self, nome):
        with open(nome+'.plk', 'rb') as arquivo:
            return pickle.load(arquivo)




def main(page: ft.Page):
    page.window_width = 630  # Define a largura da janela como 800 pixels
    page.window_height = 970  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    i =  layout_Importar( printt = saida.pprint, page = page)    
    page.add(i,saida)




if __name__ == '__main__':    
    ft.app(main) 