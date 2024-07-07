import json
import flet as ft
from operator import attrgetter

class ConfirmarSaida:
    def __init__(self, page, funcao=None):
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

    def yes_click(self, e):
        if self.funcao:
            self.funcao(e)
        self.page.window_destroy()

    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self, page):
        self.page = page
        self.page.on_resize = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
        self.page.overlay.append(self.pw)

    def page_resize(self, e):
        self.pw.value = f"{self.page.window_width}*{self.page.window_height} px"
        self.pw.update()

class Saida(ft.Column):
    def __init__(self, width=300,height=100):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad], auto_scroll=True, width=width,height=height), bgcolor='white,0.03'))

    def pprint(self, *texto):
        for i in texto:
            self.saidad.value += f'{i}\n'
        self.page.update()

class Vila(ft.Row):
    def __init__(self, nome=None, nivel_cv=None, forca=None, cv_exposto=None, equipe=None, metodo=2, mapa=None, func=None):
        super().__init__()
        self.func = func
        self._nome = ft.Dropdown(value=nome, options=[ft.dropdown.Option(i) for i in range(51)], dense=True, content_padding=5, width=60, on_change=self.Chenge_nome)
        self.cv = ft.Dropdown(focused_bgcolor=None, bgcolor=None, filled=True, value=nivel_cv, options=[ft.dropdown.Option(i) for i in range(20)], dense=True, content_padding=5, width=60, on_change=self.cor, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
        self.cor2(str(nivel_cv))
        self.exposicao = ft.Dropdown(value=cv_exposto, options=[ft.dropdown.Option(i) for i in range(2)], dense=True, content_padding=5, width=50, on_change=self.change_exposicao)
        self.controls = [self._nome, self.cv, self.exposicao]
        self.tight = True
        self.spacing = 0
        self.run_spacing = 0

        self.nome = nome
        self.nivel_cv = nivel_cv
        self.forca = forca
        self.cv_exposto = cv_exposto
        self.estrelas_l = 0
        self.atacante = 0
        self.estrela = 0
        self.metodo = metodo
        self.mapa = mapa
        self._equipe = equipe
        if isinstance(self._equipe, dict):
            self.set_equipe(self._equipe)

    def set_equipe(self, equipe):
        self.GRUPO_ELITE = int(equipe['GRUPO ELITE'])
        self.GRUPO_A = int(equipe['GRUPO A'])
        self.GRUPO_B = int(equipe['GRUPO B'])
        self.GRUPO_C = int(equipe['GRUPO C'])
        self.GRUPO_D = int(equipe['GRUPO D'])
        self.GRUPO_E = int(equipe['GRUPO E'])

    @property
    def equipe(self):
        return self._equipe

    @equipe.setter
    def equipe(self, equipe):
        self._equipe = equipe
        if isinstance(self._equipe, dict):
            self.set_equipe(self._equipe)

    def recebe_ataque(self, lista_jogadores):
        estrelas = 0
        for jogador in lista_jogadores:
            estrela_temp = 1 if self.cv_exposto == 1 else 0
            estrelas = self.calcular_estrelas(jogador, estrela_temp)
        self.estrelas_l = estrelas

    @property
    def cv_exp(self):
        return self.cv_exposto
    
    @cv_exp.setter
    def cv_exp(self, cv_exp):
        self.cv_exposto = cv_exp
        self.exposicao.value = 0


    
    def calcular_estrelas(self, jogador, estrela_temp):
        estrelas = 0
        if self.metodo == 1:
            estrelas = self.metodo_1(jogador, estrela_temp)
        elif self.metodo in [2, 4]:
            estrelas = self.metodo_2_4(jogador, estrela_temp)
        elif self.metodo == 3:
            estrelas = self.metodo_3(jogador)
        return estrelas

    def metodo_1(self, jogador, estrela_temp):
        estrelas = 0
        if jogador.nivel_cv == 15:
            estrelas = self.estrelas_para_cv_15(jogador)
        elif jogador.nivel_cv == 14:
            estrelas = self.estrelas_para_cv_14(jogador)
        elif jogador.nivel_cv == 13:
            estrelas = self.estrelas_para_cv_13(jogador)
        elif jogador.nivel_cv == 12:
            estrelas = self.estrelas_para_cv_12(jogador)
        elif jogador.nivel_cv == 11:
            estrelas = self.estrelas_para_cv_11(jogador)
        elif jogador.nivel_cv == 10:
            estrelas = self.estrelas_para_cv_10(jogador)
        elif jogador.nivel_cv == 9:
            estrelas = self.estrelas_para_cv_9(jogador)
        elif jogador.nivel_cv == 8:
            estrelas = self.estrelas_para_cv_8(jogador)
        return estrelas

    def metodo_2_4(self, jogador, estrela_temp):
        estrelas = 0
        if jogador.forca >= self.GRUPO_ELITE:
            estrelas = 3 if self.nivel_cv <= 14 else 2
        elif jogador.forca >= self.GRUPO_A:
            estrelas = 3 if self.nivel_cv <= 13 else 2
        elif jogador.forca >= self.GRUPO_B:
            estrelas = 3 if self.nivel_cv <= 12 else 2
        elif jogador.forca >= self.GRUPO_C:
            estrelas = 3 if self.nivel_cv <= 11 else (2 if self.nivel_cv in [12, 13] else estrela_temp + 1)
        elif jogador.forca >= self.GRUPO_D:
            estrelas = 3 if self.nivel_cv <= 10 else (2 if self.nivel_cv in [11, 12] else (1 + estrela_temp if self.nivel_cv == 13 else estrela_temp))
        elif jogador.forca >= self.GRUPO_E:
            estrelas = 3 if self.nivel_cv <= 9 else (2 if self.nivel_cv == 10 else (estrela_temp + 1 if self.nivel_cv == 11 else (1 if self.nivel_cv == 12 else estrela_temp)))
        return estrelas

    def metodo_3(self, jogador):
        try:
            estrelas = self.mapa.loc[str(jogador.nome), str(self.nome)]
        except:
            estrelas = self.mapa.loc[str(jogador.nome), str(self.nome) + '.0']
        return estrelas

    def estrelas_para_cv_15(self, jogador):
        if self.nivel_cv == 13:
            return 3 if jogador.forca > 90 else 2
        elif self.nivel_cv <= 12:
            return 3
        elif self.nivel_cv == 15:
            return 3 if self.forca < 40 else 2
        elif self.nivel_cv == 14:
            return 2 if self.forca > 60 else 3
        return 0

    def estrelas_para_cv_14(self, jogador):
        if self.nivel_cv <= 12:
            return 3 if jogador.forca > 50 else 2
        elif self.nivel_cv > 14:
            return 3 if self.forca < 20 else (2 if jogador.forca > 50 else 1)
        elif self.nivel_cv == 14:
            return 3 if self.forca < 40 else (2 if jogador.forca > 50 else 1)
        elif self.nivel_cv == 13:
            return 3 if jogador.forca > 90 else (3 if self.forca < 50 else 2)
        return 0

    def estrelas_para_cv_13(self, jogador):
        if self.nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self.nivel_cv == 14:
            return 3 if self.forca < 20 else 1
        elif self.nivel_cv == 13:
            return 3 if self.forca < 30 else 2
        elif self.nivel_cv == 12:
            return 3 if self.forca < 30 else 2
        elif self.nivel_cv <= 11:
            return 3
        return 0

    def estrelas_para_cv_12(self, jogador):
        if self.nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self.nivel_cv == 14:
            return 2 if self.forca < 60 else 1
        elif self.nivel_cv == 13:
            return 2 if self.forca < 50 else 1
        elif self.nivel_cv == 12:
            return 3 if self.forca < 20 else (2 if jogador.forca > 60 else 1)
        elif self.nivel_cv == 11:
            return 3 if self.forca < 30 else 2
        elif self.nivel_cv <= 10:
            return 3
        return 0

    def estrelas_para_cv_11(self, jogador):
        if self.nivel_cv > 14:
            return 2 if self.forca < 20 else 1
        elif self.nivel_cv == 14:
            return 2 if self.forca < 40 else 1
        elif self.nivel_cv == 13:
            return 2 if self.forca < 40 else 1
        elif self.nivel_cv == 12:
            return 3 if self.forca < 20 else 1
        elif self.nivel_cv == 11:
            return 3 if self.forca < 40 else 2
        elif self.nivel_cv <= 10:
            return 3
        return 0

    def estrelas_para_cv_10(self, jogador):
        if self.nivel_cv <= 9:
            return 3
        elif self.nivel_cv >= 14:
            return 1 if self.forca < 20 else 1
        elif self.nivel_cv == 13:
            return 2 if self.forca > 20 else 3
        elif self.nivel_cv == 12:
            return 2 if self.forca > 20 else 3
        elif self.nivel_cv == 11:
            return 2 if self.forca > 20 else 3
        elif self.nivel_cv == 10:
            return 2 if self.forca > 80 else 3
        return 0

    def estrelas_para_cv_9(self, jogador):
        if self.nivel_cv <= 8:
            return 3
        elif self.nivel_cv == 12:
            return 1 if self.forca < 20 else 0
        elif self.nivel_cv == 10:
            return 2 if self.forca > 50 else 3
        elif self.nivel_cv == 9:
            return 2 if jogador.forca < 90 else 3
        return 0

    def estrelas_para_cv_8(self, jogador):
        if self.nivel_cv <= 8:
            return 3
        elif self.nivel_cv >= 11:
            return 1 if self.forca < 20 else 0
        elif self.nivel_cv == 10:
            return 1 if self.forca > 50 else 2
        elif self.nivel_cv == 9:
            return 2
        return 0

    def Chenge_nome(self, e):
        self.nome = int(self._nome.value)
        if self.func:
            self.func(int(self.cv.value))

    def change_exposicao(self, e):
        self.cv_exposto = int(self.exposicao.value)
        if self.func:
            self.func(int(self.cv.value))

    def cor(self, e):
        self.cv.color = None
        self.update()
        self.cor2(e.control.value)
        self.nivel_cv = int(self.cv.value)
        if self.func:
            self.func(int(self.cv.value))
        self.update()

    def cor2(self, cv):
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }
        self.cv.bgcolor = colors.get(cv, None)
        if cv in ['14', '13', '12', '11', '10', '9', '8']:
            self.cv.color = 'red'

class LayoutVilas(ft.Column):
    def __init__(self, num_vilas=15, printt=None, page=None):
        super().__init__()
        self.printt = printt
        self.page = page
        self.num_vilas = ft.Dropdown(label='Número de Vilas', value=num_vilas, options=[ft.dropdown.Option(i) for i in range(51)], dense=True, content_padding=5, width=180, on_change=self.Chenge_num_vilas)
        self.botao_salvar = ft.ElevatedButton('Salvar', on_click=self.Salvar, width=150)
        self.botao_zerar = ft.ElevatedButton('zerar exp', on_click=self.Zerar_exposicoes, width=150)
        self.botao_ordenar = ft.ElevatedButton('Ordenar', on_click=self.Ordenar_vilas, width=150)

        self.controls.extend([
            self.num_vilas,
            ft.Row([self.botao_salvar,self.botao_zerar,self.botao_ordenar]),
            ft.Container(ft.Row([ft.Text('  Nome    '), ft.Text(' CV  '), ft.Text('Exposição')]), border=ft.border.all(1, 'white,0.5'), width=180)
        ])
        cumprimento_coluna = min(540, 165 + (36 * int(num_vilas)))
        self.controls.append(ft.Container(ft.Column(height=cumprimento_coluna, scroll=ft.ScrollMode.ADAPTIVE), border=ft.border.all(1, 'white,0.5'), width=180))

        self.lista_vilas = self.inicializar_vilas()
        self.controls[3].content.controls = self.lista_vilas

    def inicializar_vilas(self):
        lista_vilas = []
        try:
            arquiv = self.Ler_json('vilas_config')
            for nome, nivel_cv, cv_exposto in zip(arquiv['nome'], arquiv['nivel_cv'], arquiv['cv_exposto']):
                lista_vilas.append(Vila(nome=nome, nivel_cv=nivel_cv, cv_exposto=cv_exposto, func=self.Salvar))
        except:
            lista_vilas = [Vila(nome=i, nivel_cv=15, cv_exposto=0, func=self.Salvar) for i in range(1, int(self.num_vilas.value) + 1)]
        return lista_vilas

    def Gera_Lista_de_Vilas(self, equipee=None):
        for vila in self.lista_vilas:
            vila.equipe = equipee
            vila.forca = (50 - vila.nome) + 50 * vila.nivel_cv
        self.printt('Lista de vilas gerada com sucesso!')
        return self.lista_vilas
        
    def Chenge_num_vilas(self, e):
            # self.page.window_height = 165+(36*int(self.num_vilas.value)) 
            self.controls[3].content.controls = []  
            self.controls[3].content.controls.append(ft.Container(ft.Row([ft.Text('  Nome    '),ft.Text(' CV  '),ft.Text('Exposição')]),border=ft.border.all(1,'white,0.5'),width=180))
            self.lista_vilas = []
            try:
                self.arquiv = self.Ler_json('vilas_config')
                if int(self.num_vilas.value) <= len(self.arquiv['nome']):
                    for i,j,k,l in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['cv_exposto'], range(1,int(self.num_vilas.value)+1)):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = j,cv_exposto = k, func=self.Salvar))
                else:
                    for i,j,k,l in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['cv_exposto'], range(1,int(self.num_vilas.value)+1)):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = j,cv_exposto = k, func=self.Salvar))  
                    for i  in range(l+1,int(self.num_vilas.value)+1):
                        self.lista_vilas.append(Vila(nome = i,nivel_cv = 15,cv_exposto = 0, func=self.Salvar))                     
            except:
                for i in range(1,int(self.num_vilas.value)+1):
                    self.lista_vilas.append(Vila(nome = i,nivel_cv = 15,cv_exposto = 0, func=self.Salvar))        
            
            self.controls[3].content.controls = self.lista_vilas   
            self.page.update()    
        



    def Zerar_exposicoes(self,e):
        for i in self.lista_vilas:
            i.cv_exp = 0
        self.controls[3].content.controls = self.lista_vilas
        self.update()

    def Salvar(self, e):
        dic = {'nome': [], 'nivel_cv': [], 'cv_exposto': []}
        for vila in self.lista_vilas:
            dic['nome'].append(vila.nome)
            dic['nivel_cv'].append(vila.nivel_cv)
            dic['cv_exposto'].append(vila.cv_exposto)
        self.Escrever_json(dic, 'vilas_config')
        self.printt('Vilas salvas com sucesso')

    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if not nomedoarquivo.endswith('json'):
            nomedoarquivo += '.json'
        with open(nomedoarquivo, 'w') as f:
            json.dump(nomedodicionario, f, indent=4)

    def Ler_json(self, nomedoarquivo):
        if not nomedoarquivo.endswith('json'):
            nomedoarquivo += '.json'
        try:
            with open(nomedoarquivo, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {}
        

    def OrdenarListadeClasses(self, lista, atributo, decrecente=True):
        return sorted(lista, key=attrgetter(atributo), reverse=decrecente)    

    def Ordenar_vilas(self, e):
        self.controls[3].content.controls = self.OrdenarListadeClasses(self.controls[3].content.controls,'nivel_cv')
        self.update()     


def main(page: ft.Page):
    page.window_width = 350
    page.window_height = 800
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START
    # page.theme = ft.ThemeMode.DARK
    ConfirmarSaida(page)
    saida = Saida(360,50)
    Resize(page)
    v = LayoutVilas(15, printt=saida.pprint, page=page)
    # page.add(ft.Row([ft.Column([v]), ft.Column([saida], alignment='center', width=150, height=600)]))
    page.add(v, saida)

if __name__ == '__main__':
    ft.app(main)
