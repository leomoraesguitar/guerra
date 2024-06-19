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


class Vila(ft.Row):
    def __init__(self, 
                 nome = None, 
                 nivel_cv = None, 
                 forca = None, 
                 cv_exposto = None, 
                 equipe = None, 
                 metodo=2, 
                 mapa=None,
                 func = None
                 
                 
                 
                 ):
        super().__init__()   
        self.func = func
        self._nome = ft.Dropdown(value = nome, options=[ft.dropdown.Option(i) for i in range(51)],dense=True, content_padding=5, width=60, on_change=self.Chenge_nome)
        self.cv = ft.Dropdown(focused_bgcolor = None, bgcolor = None,filled = True,value = nivel_cv, options=[ft.dropdown.Option(i) for i in range(20)],dense=True, content_padding=5, width=60, on_change=self.cor, text_style = ft.TextStyle(weight = ft.FontWeight.BOLD) )
        self.cor2(str(nivel_cv))
        self.exposicao = ft.Dropdown(value = cv_exposto, options=[ft.dropdown.Option(i) for i in range(2)],dense=True, content_padding=5, width=50, on_change=self.change_exposicao)
        self.controls = [self._nome,self.cv, self.exposicao ]
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
        # self._equipes_iniciadas = self.Iniciar_equipe()
        ''' Equipes'''
        if isinstance(self._equipe, dict):
            self.GRUPO_ELITE = int(self._equipe['GRUPO ELITE'])
            self.GRUPO_A = int(self._equipe['GRUPO A'])
            self.GRUPO_B = int(self._equipe['GRUPO B'])
            self.GRUPO_C = int(self._equipe['GRUPO C'])
            self.GRUPO_D = int(self._equipe['GRUPO D'])
            self.GRUPO_E = int(self._equipe['GRUPO E'])


    @property
    def equipe(self):
        return self._equipe
    @equipe.setter
    def equipe(self,equipe):
        self._equipe = equipe
        if isinstance(self._equipe, dict):
            self.GRUPO_ELITE = int(self._equipe['GRUPO ELITE'])
            self.GRUPO_A = int(self._equipe['GRUPO A'])
            self.GRUPO_B = int(self._equipe['GRUPO B'])
            self.GRUPO_C = int(self._equipe['GRUPO C'])
            self.GRUPO_D = int(self._equipe['GRUPO D'])
            self.GRUPO_E = int(self._equipe['GRUPO E'])

            

    def recebe_ataque(self, lista_jogadores):

        if self.metodo == 1:
            estrelas = 0
            for jogador in lista_jogadores:
                # print('nível do cv do jogador', jogador.nivel_cv)
                # print('nível do cv da vila', self.nivel_cv)
                # diferença_de_cv = jogador.nivel_cv - self.nivel_cv
                # if mostrar_ataques ==1:
                #   print(f'{jogador.nome} - cv{jogador.nivel_cv} atacando:')
                estrela_temp = 0
                if self.cv_exposto == 1:
                    estrela_temp = 1
                # cv do jogador =15

                if jogador.nivel_cv == 15:
                    if self.nivel_cv == 13:
                        if jogador.forca > 90:
                            estrelas = 3
                        else:
                            estrelas = 2
                    if self.nivel_cv <= 12:
                        estrelas = 3
                    elif self.nivel_cv == 15:
                        if self.forca < 40:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv == 14:
                        if self.forca > 60:
                            estrelas = 2
                        else:
                            estrelas = 3

                # cv do jogador =14   #################################################
                elif jogador.nivel_cv == 14:
                    if self.nivel_cv <= 12:
                        if jogador.forca > 50:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv > 14:
                        if self.forca < 20:
                            estrelas = 3
                        else:
                            if jogador.forca > 50:
                                estrelas = 2
                            else:
                                estrelas = estrela_temp + 1
                    elif self.nivel_cv == 14:
                        if self.forca < 40:
                            estrelas = 3
                        else:
                            if jogador.forca > 50:
                                estrelas = 2
                            else:
                                estrelas = estrela_temp + 1

                    elif self.nivel_cv == 13:
                        if jogador.forca > 90:
                            estrelas = 3
                        else:
                            if self.forca < 50:
                                estrelas = 3
                            else:
                                estrelas = 2

                # cv do jogador =13    #################################################
                elif jogador.nivel_cv == 13:
                    if self.nivel_cv > 14:
                        if self.forca < 20:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp + 1
                    elif self.nivel_cv == 14:
                        if self.forca < 20:
                            estrelas = 3
                        else:
                            estrelas = estrela_temp + 1
                    elif self.nivel_cv == 13:
                        if self.forca < 30:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv == 12:
                        if self.forca < 30:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv <= 11:
                        estrelas = 3
                # cv do jogador =12   #################################################
                elif jogador.nivel_cv == 12:
                    if self.nivel_cv > 14:
                        if self.forca < 20:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 14:
                        if self.forca < 60:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 13:
                        if self.forca < 50:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp + 1
                    elif self.nivel_cv == 12:
                        if self.forca < 20:
                            estrelas = 3
                        else:
                            if jogador.forca > 60:
                                estrelas = 2
                            else:
                                estrelas = estrela_temp + 1
                    elif self.nivel_cv == 11:
                        if self.forca < 30:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv <= 10:
                        estrelas = 3

                # cv do jogador =11   #################################################
                elif jogador.nivel_cv == 11:
                    if self.nivel_cv > 14:
                        if self.forca < 20:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 14:
                        if self.forca < 40:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 13:
                        if self.forca < 40:
                            estrelas = 2
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 12:
                        if self.forca < 20:
                            estrelas = 3
                        else:
                            estrelas = estrela_temp + 1
                    elif self.nivel_cv == 11:
                        if self.forca < 40:
                            estrelas = 3
                        else:
                            estrelas = 2
                    elif self.nivel_cv <= 10:
                        estrelas = 3
                # cv do jogador =10   #################################################
                elif jogador.nivel_cv == 10:
                    if self.nivel_cv <= 9:
                        estrelas = 3
                    elif self.nivel_cv >= 14:
                        if self.forca < 20:
                            estrelas = estrela_temp + 1
                        else:
                            estrelas = 1
                    elif self.nivel_cv == 13:
                        if self.forca > 20:
                            estrelas = 2
                        else:
                            estrelas = 3
                    elif self.nivel_cv == 12:
                        if self.forca > 20:
                            estrelas = 2
                        else:
                            estrelas = 3
                    elif self.nivel_cv == 11:
                        if self.forca > 20:
                            estrelas = 2
                        else:
                            estrelas = 3
                    elif self.nivel_cv == 10:
                        if self.forca > 80:
                            estrelas = 2
                        else:
                            estrelas = 3

                # cv do jogador =9   #################################################
                elif jogador.nivel_cv == 9:
                    if self.nivel_cv <= 8:
                        estrelas = 3
                    elif self.nivel_cv == 12:
                        if self.forca < 20:
                            estrelas = estrela_temp + 1
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 10:
                        if self.forca > 50:
                            estrelas = 2
                        else:
                            estrelas = 3
                    elif self.nivel_cv == 9:
                        if jogador.forca < 90:
                            estrelas = 2
                        else:
                            estrelas = 3

                elif jogador.nivel_cv == 8:
                    if self.nivel_cv <= 8:
                        estrelas = 3
                    elif self.nivel_cv >= 11:
                        if self.forca < 20:
                            estrelas = estrela_temp + 1
                        else:
                            estrelas = estrela_temp
                    elif self.nivel_cv == 10:
                        if self.forca > 50:
                            estrelas = estrela_temp + 1
                        else:
                            estrelas = 2
                    elif self.nivel_cv == 9:
                        estrelas = 2

                # if mostrar_ataques ==1:
                #   print(f'Vila {self.nome} (cv {self.nivel_cv}) faz {estrelas} estrelas')
                self.estrelas_l = estrelas

        if self.metodo in [2, 4]:
            estrelas = 0
            for jogador in lista_jogadores:
                # print('nível do cv do jogador', jogador.nivel_cv)
                # print('força do jogador', jogador.forca)
                # print('nível do cv da vila', self.nivel_cv)
                # diferença_de_cv = jogador.nivel_cv - self.nivel_cv
                # if mostrar_ataques ==1:
                #   print(f'{jogador.nome} - cv{jogador.nivel_cv} atacando:')
                estrela_temp = 0
                if self.cv_exposto == 1:
                    estrela_temp = 1
                # cv do jogador =15

                # GRUPO_ELITE = 989
                # GRUPO_A = 910
                # GRUPO_B = 840
                # GRUPO_C = 675
                # GRUPO_D = 579
                # GRUPO_E = 510

                if jogador.forca >= self.GRUPO_ELITE:
                    if self.nivel_cv <= 14:
                        estrelas = 3
                    if self.nivel_cv > 14:
                        estrelas = 2

                if jogador.forca >= self.GRUPO_A and jogador.forca < self.GRUPO_ELITE:
                    if self.nivel_cv <= 13:
                        estrelas = 3
                    if self.nivel_cv > 13:
                        estrelas = 2

                elif jogador.forca >= self.GRUPO_B and jogador.forca < self.GRUPO_A:
                    if self.nivel_cv <= 12:
                        estrelas = 3
                    if self.nivel_cv > 12:
                        estrelas = 2

                elif jogador.forca >= self.GRUPO_C and jogador.forca < self.GRUPO_B:
                    if self.nivel_cv <= 11:
                        estrelas = 3
                    if self.nivel_cv in [12, 13]:
                        estrelas = 2
                    if self.nivel_cv >= 14:
                        estrelas = estrela_temp + 1

                elif jogador.forca >= self.GRUPO_D and jogador.forca < self.GRUPO_C:
                    if self.nivel_cv <= 10:
                        estrelas = 3
                    if self.nivel_cv == 11:
                        estrelas = 2
                    if self.nivel_cv == 12:
                        estrelas = 2
                    if self.nivel_cv == 13:
                        estrelas = 1 + estrela_temp
                    if self.nivel_cv >= 14:
                        estrelas = estrela_temp

                elif jogador.forca >= self.GRUPO_E and jogador.forca < self.GRUPO_D:
                    if self.nivel_cv <= 9:
                        estrelas = 3
                    if self.nivel_cv == 10:
                        estrelas = 2
                    if self.nivel_cv == 11:
                        estrelas = estrela_temp + 1
                    if self.nivel_cv == 12:
                        estrelas = 1
                    if self.nivel_cv >= 13:
                        estrelas = estrela_temp

                # if mostrar_ataques ==1:
                #   print(f'Vila {self.nome} (cv {self.nivel_cv}) faz {estrelas} estrelas')
                # print(f'{jogador.forca} fez {self.estrelas_l} na vila {self.nome}')
            self.estrelas_l = estrelas

        if self.metodo == 3:
            estrelas = 0
            for jogador in lista_jogadores:
                plan = self.mapa
                # print(plan)
                try:
                    estrelas = plan.loc[str(jogador.nome), str(self.nome)]
                except:
                    estrelas = plan.loc[str(jogador.nome), str(self.nome)+'.0']
            self.estrelas_l = estrelas

    def Chenge_nome(self,e):
        self.nome = int(self._nome.value)
        if self.func != None:
            self.func(int(self.cv.value))
    def change_exposicao(self, e):
        self.cv_exposto = int(self.exposicao.value)
        if self.func != None:
            self.func(int(self.cv.value))
    def cor(self,e):
        self.cv.color = None
        self.update()

        match e.control.value:
            case '16':
                self.cv.bgcolor = 'red'
            case '15':
                self.cv.bgcolor = '#ff9900'
            case '14':
                self.cv.bgcolor = '#ffd966'
                self.cv.color = 'red'

            case '13':
                self.cv.bgcolor = '#93c47d'
                self.cv.color = 'red'

            case '12':
                self.cv.bgcolor = '#ea9999'  
                self.cv.color = 'red'

            case '11':
                self.cv.bgcolor = '#ffff00'
                self.cv.color = 'red'
            case '10':
                self.cv.bgcolor = '#d9ead3'
                self.cv.color = 'red'                        
            case '9':
                self.cv.bgcolor = '#c9daf8'
                self.cv.color = 'red'                        
            case '8':
                self.cv.bgcolor = '#d9d9d9'                                                                                                
                self.cv.color = 'red'
        self.nivel_cv = int(self.cv.value)
        if self.func != None:
            self.func(int(self.cv.value))
        self.update()
    
    def cor2(self,cv):
        match cv:
            case '16':
                self.cv.bgcolor = 'red'
            case '15':
                self.cv.bgcolor = '#ff9900'
            case '14':
                self.cv.bgcolor = '#ffd966'
                self.cv.color = 'red'

            case '13':
                self.cv.bgcolor = '#93c47d'
                self.cv.color = 'red'

            case '12':
                self.cv.bgcolor = '#ea9999' 
                self.cv.color = 'red'

            case '11':
                self.cv.bgcolor = '#ffff00'
                self.cv.color = 'red'
            case '10':
                self.cv.bgcolor = '#d9ead3'
                self.cv.color = 'red'                        
            case '9':
                self.cv.bgcolor = '#c9daf8'
                self.cv.color = 'red'                        
            case '8':
                self.cv.bgcolor = '#d9d9d9'                                                                                                
                self.cv.color = 'red'

#122 - 158 = -36
class layout_vilas(ft.Column):
    def __init__(self, num_vilas = 15, printt = None, page = None):
        super().__init__()
        self.printt = printt
        self.page = page

        # if self.page != None:
        #     self.page.window_height = 165+(36*int(num_vilas))

        self.num_vilas = ft.Dropdown(label = 'Número de Vilas',value = num_vilas, options=[ft.dropdown.Option(i) for i in range(51)],dense=True, content_padding=5, width=180, on_change=self.Chenge_num_vilas)
       
        '''       
        # class Nomecvexposicao(ft.Row):
        #     def __init__(self,nome,cv,exposicao):
        #         super().__init__()   
        #         self.nome = ft.Dropdown(value = nome, options=[ft.dropdown.Option(i) for i in range(31)],dense=True, content_padding=5, width=60)
        #         self.cv = ft.Dropdown(bgcolor = 'black',filled = True,value = cv, options=[ft.dropdown.Option(i) for i in range(20)],dense=True, content_padding=5, width=60, on_change=self.cor)
        #         self.cor2(str(cv))
        #         self.exposicao = ft.Dropdown(value = exposicao, options=[ft.dropdown.Option(i) for i in range(1)],dense=True, content_padding=5, width=50)
        #         self.controls = [self.nome,self.cv, self.exposicao ]
        #         self.tight = True
        #         self.spacing = 0
        #         self.run_spacing = 0
        #     def cor(self,e):
        #         match e.control.value:
        #             case '16':
        #                 self.cv.bgcolor = 'red'
        #             case '15':
        #                 self.cv.bgcolor = '#ff9900'
        #             case '14':
        #                 self.cv.bgcolor = '#ffd966'
        #             case '13':
        #                 self.cv.bgcolor = '#93c47d'
        #             case '12':
        #                 self.cv.bgcolor = '#ea9999'                                                                                                
        #             case '11':
        #                 self.cv.bgcolor = '#ffff00'
        #                 self.cv.color = 'black'
        #             case '10':
        #                 self.cv.bgcolor = '#d9ead3'
        #                 self.cv.color = 'black'                        
        #             case '9':
        #                 self.cv.bgcolor = '#c9daf8'
        #                 self.cv.color = 'black'                        
        #             case '8':
        #                 self.cv.bgcolor = '#d9d9d9'                                                                                                
        #                 self.cv.color = 'black'

        #         self.update()
        #     def cor2(self,cv):
        #         match cv:
        #             case '16':
        #                 self.cv.bgcolor = 'red'
        #             case '15':
        #                 self.cv.bgcolor = '#ff9900'
        #             case '14':
        #                 self.cv.bgcolor = '#ffd966'
        #             case '13':
        #                 self.cv.bgcolor = '#93c47d'
        #             case '12':
        #                 self.cv.bgcolor = '#ea9999'                                                                                                
        #             case '11':
        #                 self.cv.bgcolor = '#ffff00'
        #                 self.cv.color = 'black'
        #             case '10':
        #                 self.cv.bgcolor = '#d9ead3'
        #                 self.cv.color = 'black'                        
        #             case '9':
        #                 self.cv.bgcolor = '#c9daf8'
        #                 self.cv.color = 'black'                        
        #             case '8':
        #                 self.cv.bgcolor = '#d9d9d9'                                                                                                
        #                 self.cv.color = 'black'
        '''
        self.botao_salvar = ft.ElevatedButton('Salvar', on_click=self.Salvar, width=180)

        self.controls.append(self.num_vilas,)
        self.controls.append(self.botao_salvar)
        self.controls.append(ft.Container(ft.Row([ft.Text('  Nome    '),ft.Text(' CV  '),ft.Text('Exposição')]),border=ft.border.all(1,'white,0.5'),width=180))
        if 165+(36*int(num_vilas)) > 540:
            cumprimento_coluna = 540 
        else:
            cumprimento_coluna = 165+(36*int(num_vilas)) 
        self.controls.append(ft.Container(ft.Column(height=cumprimento_coluna, scroll=ft.ScrollMode.ADAPTIVE),border=ft.border.all(1,'white,0.5'),width=180))

        
        self.lista_vilas = []
        try:
            self.arquiv = self.Ler_json('vilas_config')
            for i,j,k in zip(self.arquiv['nome'],self.arquiv['nivel_cv'],self.arquiv['cv_exposto']):
                self.lista_vilas.append(Vila(nome = i,nivel_cv = j,cv_exposto = k, func=self.Salvar))

        except:
            print('deu erro na importação das vilas')
            for i in range(1,int(self.num_vilas.value)+1):
                self.lista_vilas.append(Vila(nome = i,nivel_cv = 15,cv_exposto = 0, func=self.Salvar))

        self.controls[3].content.controls = self.lista_vilas

    def Gera_Lista_de_Vilas(self, equipee = None):
        for i in self.lista_vilas:
            i.equipe = equipee
            forca = (50-i.nome)+50*(i.nivel_cv)
            i.forca = forca

        self.printt('Lista de vilas gerada com sucesso!')
        # self.printt(self.lista_vilas[0].__dict__)

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



    def Salvar(self,e):
        dic = {'nome':[],'nivel_cv':[],'cv_exposto':[] }
        for i in self.controls[3].content.controls:
            dic['nome'].append(i.nome)
            dic['nivel_cv'].append(i.nivel_cv)
            dic['cv_exposto'].append(i.cv_exposto)
        
        self.Escrever_json(dic, 'vilas_config')
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
    page.window_height = 705  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    v =  layout_vilas(15, printt = saida.pprint, page = page)    
    page.add(ft.Row([ft.Column([v]),ft.Column([saida],alignment='center', width=150, height=600)]))




if __name__ == '__main__':    
    ft.app(main,
    #    view = ft.AppView.WEB_BROWSER
    # port = 8050
       )