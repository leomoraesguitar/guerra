


import json
import flet as ft

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


class Jogador(ft.Row):
    def __init__(self, nome, nivel_cv, forca):
        super().__init__()
        self.peso = 0
        nomes = ('Cristiano',
 'lulmor',
 'lllll',
 'leoclash10',
"cacauesntos",
"rochaleo",
"lolop",
"Diogo SvS",
"SR.ALEXANDRE",
"GOKU BL4CKSE",
"xXBPCBXx",
 'Letícia',
 'MaggieMelT',
 'GERIEL CAOS',
 'br')
        
        # self._nome = ft.Dropdown(value = nome, options=[ft.dropdown.Option(i) for i in nomes],dense=True, content_padding=5, width=130)
        self._nome = ft.Text(value = nome,  width=130)
        # self._nivel_cv = ft.Dropdown(focused_bgcolor = None, bgcolor = None,filled = True,value = nivel_cv, options=[ft.dropdown.Option(i) for i in range(20)],dense=True, content_padding=5, width=60,  text_style = ft.TextStyle(weight = ft.FontWeight.BOLD) )
        self._nivel_cv = ft.Text(value = nivel_cv,  width=60, )
        # self._forca = ft.TextField(value = forca, dense=True, content_padding=5, width=60)
        self._forca = ft.Text(value = forca,  width=60)
        # self._estrelas = None
        self.controls = [self._nome,self._nivel_cv, self._forca ]
    
    @property
    def nome(self):
        return self._nome.value
    @nome.setter
    def nome(self,nome):
        self._nome.value = nome

    @property
    def nivel_cv(self):
        return int(self._nivel_cv.value)
    @nivel_cv.setter
    def nivel_cv(self, nivel):
        self._nivel_cv.value = int(nivel)

    @property
    def forca(self):
        return int(self._forca.value)
    @forca.setter
    def forca(self, forca):
        self._forca.value = int(forca)

    # @property
    # def estrelas(self):
    #     return self._estrelas.value
    # @estrelas.setter
    # def estrelas(self,estrelas):
    #     self._estrelas.value = estrelas        


class layout_jogadores(ft.Column):
    def __init__(self, num_jogadores = 15, printt = None, page = None):
        super().__init__()
        self.printt = printt
        self.num_jogadores = ft.Dropdown(label = 'Número de Jogadores',value = num_jogadores, 
                options=[ft.dropdown.Option(i) for i in range(5,51)],dense=True, 
                content_padding=5, width=180, on_change=self.Chenge_num_jogadores)
        self.botao_salvar = ft.ElevatedButton('Salvar', on_click=self.Salvar, width=180)
        self.botao_atualizar = ft.ElevatedButton('Atualizar', on_click=self.Atualizar, width=180)
        self.controls.append(self.num_jogadores)
        self.controls.append(self.botao_atualizar)
        self.controls.append(ft.Container(ft.Row([ft.Text('           Nome           '),ft.Text(' CV         '),ft.Text('forca')]),border=ft.border.all(1,'white,0.5'),width=300))
        
        if 165+(36*int(num_jogadores)) > 540:
            cumprimento_coluna = 540 
        else:
            cumprimento_coluna = 165+(36*int(num_jogadores)) 
        self.controls.append(ft.Column(height=cumprimento_coluna, scroll=ft.ScrollMode.ADAPTIVE))

        
        self.lista_jogadores = []
        try:
            self.arquiv = self.Ler_json('jogadores_config')
            for i,j,k in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['forca']):
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = j,forca = k))

        except:
            print('deu erro na importação dos jogadores')
            nomes = ('Cristiano',
                    'lulmor',
                    'lllll',
                    'leoclash10',
                    "cacauesntos",
                    "rochaleo",
                    "lolop",
                    "Diogo SvS",
                    "SR.ALEXANDRE",
                    "GOKU BL4CKSE",
                    "xXBPCBXx",
                    'Letícia',
                    'MaggieMelT',
                    'GERIEL CAOS',
                    'br')            
            for i in nomes:
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = 15,forca = 800))

        self.controls[3].controls = self.lista_jogadores

    def Atualizar(self,e):
        self.lista_jogadores = []
        try:
            self.arquiv = self.Ler_json('jogadores_config')
            for i,j,k in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['forca']):
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = j,forca = k))

        except:
            print('deu erro na importação dos jogadores')
            nomes = ('Cristiano',
                    'lulmor',
                    'lllll',
                    'leoclash10',
                    "cacauesntos",
                    "rochaleo",
                    "lolop",
                    "Diogo SvS",
                    "SR.ALEXANDRE",
                    "GOKU BL4CKSE",
                    "xXBPCBXx",
                    'Letícia',
                    'MaggieMelT',
                    'GERIEL CAOS',
                    'br')            
            for i in nomes:
                self.lista_jogadores.append(Jogador(nome = i,nivel_cv = 15,forca = 800))

        self.controls[3].controls = self.lista_jogadores
        self.update()

    def Gera_Lista_de_jogadores(self):
        return self.lista_jogadores


    def Chenge_num_jogadores(self, e):  
        pass   
    def Salvar(self,e):
        dic = {'nome':[],'nivel_cv':[],'forca':[] }
        for i in self.controls[3].controls:
            dic['nome'].append(i.nome)
            dic['nivel_cv'].append(i.nivel_cv)
            dic['forca'].append(i.forca)
        
        self.Escrever_json(dic, 'jogadores_config')
        self.printt('Vilas salvas com sucesso')


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

def main(page: ft.Page):
    page.window_width = 380  # Define a largura da janela como 800 pixels
    page.window_height = 900  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    j =  layout_jogadores(15, printt = saida.pprint, page = page)    
    page.add(j,saida)




if __name__ == '__main__':    
    ft.app(main)        